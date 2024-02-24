import os
import shutil
from urllib.parse import unquote, urlparse

import supervisely as sly
from cv2 import connectedComponents
from dataset_tools.convert import unpack_if_archive
from supervisely.io.fs import file_exists, get_file_name, get_file_name_with_ext
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    ### Function should read local dataset and upload it to Supervisely project, then return project info.###
    images_path = "/home/alex/DATASETS/TODO/MJU-Waste/mju-waste-v1.0/JPEGImages"
    batch_size = 30
    group_tag_name = "im_id"

    train_split_path = (
        "/home/alex/DATASETS/TODO/MJU-Waste/mju-waste-v1.0/ImageSets/Segmentation/train.txt"
    )
    val_split_path = (
        "/home/alex/DATASETS/TODO/MJU-Waste/mju-waste-v1.0/ImageSets/Segmentation/val.txt"
    )
    test_split_path = (
        "/home/alex/DATASETS/TODO/MJU-Waste/mju-waste-v1.0/ImageSets/Segmentation/test.txt"
    )

    ds_name_to_split = {"train": train_split_path, "val": val_split_path, "test": test_split_path}
    images_ext = ".png"

    def create_ann(image_path):
        labels = []
        tags = []

        group_id = sly.Tag(group_tag_meta, value=get_file_name(image_path)[:-6])
        tags.append(group_id)

        # image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = 480  # image_np.shape[0]
        img_wight = 640  # image_np.shape[1]

        mask_path = image_path.replace("JPEGImages", "SegmentationClass")

        if file_exists(mask_path):
            # mask_np = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
            mask_np = sly.imaging.image.read(mask_path)[:, :, 0]
            mask = mask_np != 0
            ret, curr_mask = connectedComponents(mask.astype("uint8"), connectivity=8)
            for i in range(1, ret):
                obj_mask = curr_mask == i
                bitmap = sly.Bitmap(data=obj_mask)
                label = sly.Label(bitmap, waste)
                labels.append(label)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=tags)

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)

    waste = sly.ObjClass("waste", sly.Bitmap)

    group_tag_meta = sly.TagMeta(group_tag_name, sly.TagValueType.ANY_STRING)

    meta = sly.ProjectMeta(
        obj_classes=[waste],
        tag_metas=[group_tag_meta],
    )
    api.project.update_meta(project.id, meta.to_json())
    api.project.images_grouping(id=project.id, enable=True, tag_name=group_tag_name)

    for ds_name, split_path in ds_name_to_split.items():
        dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

        images_names = []
        with open(split_path) as f:
            content = f.read().split("\n")
            for curr_data in content:
                if len(curr_data) != 0:
                    images_names.append(curr_data + images_ext)

        progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

        for img_names_batch in sly.batched(images_names, batch_size=batch_size):
            images_pathes_batch = []
            images_names_batch = []
            for im_name in img_names_batch:
                images_names_batch.append(get_file_name_with_ext(im_name))
                im_path = os.path.join(images_path, im_name)
                images_pathes_batch.append(im_path)

                images_names_batch.append(im_name.replace("color", "depth"))
                depth_path = im_path.replace("JPEGImages", "DepthImages").replace("color", "depth")
                images_pathes_batch.append(depth_path)

            img_infos = api.image.upload_paths(dataset.id, images_names_batch, images_pathes_batch)
            img_ids = [im_info.id for im_info in img_infos]

            anns = []
            for i in range(0, len(images_pathes_batch), 2):
                ann = create_ann(images_pathes_batch[i])
                anns.extend([ann, ann])
            api.annotation.upload_anns(img_ids, anns)

            progress.iters_done_report(len(images_names_batch))

    return project
