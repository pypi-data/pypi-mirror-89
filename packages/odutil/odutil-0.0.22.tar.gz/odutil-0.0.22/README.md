# odutil
Object Detection Utils

## analysis
```python
from odutil import analysis

analysis.parse_anno(path_anno):
    """
    Parse an annotation file into a dict.

    Args:
        path_anno: The path of the annotation file you wanna parse.

    Returns:
        A dict mapping filename, size and objects in the annotation to the
        corresponding data fetched.
        For example:

        {'filename': 'image.jpg',
         'size': {'width': '1621', 'height': '1216', 'depth': '3'},
         'object': [
             {'name': 'class1', 'xmin': '904', 'ymin': '674', 'xmax': '926', 'ymax': '695'},
             {'name': 'class2', 'xmin': '972', 'ymin': '693', 'xmax': '993', 'ymax': '713'}]}
    """

analysis.parse_annos(path_anno_folder):
    """
    Parse a list of annotation files into a list of dicts.

    Args:
        path_anno: The directory of the annotation files you wanna parse.

    Returns:
        A dict of dicts. Each of them mapping annotation file name("annoname")
        to the corresponding annotation dict fetched by parse_anno().
    """

analysis.check_match(path_1, path_2):
    """
    Check if the file names in the folders match each other.

    Param:
        path_1: Path of a folder.
        path_2: Path of another folder.

    Return:
        True if match else False.
    """

analysis.gen_label(path_anno, path_names, path_out):
    """
    Generate label txt from annotation.

    Args:
        path_anno: Path of the annotation file.
        path_names: Path of the .names file.
        path_out: Path of the output .txt file.

    Returns:
        None
    """

analysis.gen_labels(path_anno_folder, path_names, path_out):
    """
    Generate label txt from a list of annotations.

    Args:
        path_anno_folder: Path of the annotation files folder.
        path_names: Path of the .names file.
        path_out: Path of the output .txt file.

    Returns:
        None
    """

analysis.bbox_distribution(path_anno_folder, verbose=0):
    """
    Analysis the bbox distribution by a list of annotation files.

    Args:
        path_anno_folder: Path of the annotation files folder.

    Returns：
        A dict contains the result.
    """

```

## visual
```python
from odutil import visual

visual.draw_bbox(img, *args):
    """
    Draw the bounding box on an image.

    Args:
        img: An image instance obtained by cv2.imread.
        args: {cls_, x, y, w, h, color_bbox, color_text}.
            cls_ is object class name.
            x, y are the coordinates of the bbox top-left corner.
            w, h are the weight and height of the bbox.
            color_bbox is the (B, G, R) color for bbox.
            color_bbox is the (B, G, R) color for text.

    Returns:
        The img with bbox on it.
    """

visual.draw_anno(path_img, path_anno, path_out, verbose=0):
    """
    Draw the bounding box of on an image by its annotation file.

    Args:
        path_img: Path of the image.
        path_anno: Path of the corresponding annotation file.
        path_out: Path of the output folder.

    Return:
        None
    """

visual.draw_annos(path_img_folder, path_anno_folder, path_out, verbose=0):
    """
    Draw the bounding box of on a list of images by their annotation files.

    Args:
        path_img_folder: Path of the images folder.
        path_anno_folder: Path of the corresponding annotation folder.
        path_out: Path of the output folder.

    Return:
        None
    """

visual.drwa_result(path_result, path_img_folder, path_out, verbose=0):
    """
    Draw the bounding box by a result file.
    The result file format is as follow:
        ...... /xxx/xxx/xxx.jpg: ......
        ...... /xxx/xxx/xxx.jpg: ......
        class_name: 75%	(left_x:  626   top_y:  961   width:   50   height:   18)
        class_name: 84%	(left_x:  626   top_y:  943   width:   47   height:   20)
    """
```