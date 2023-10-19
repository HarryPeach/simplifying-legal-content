import zipfile
from os.path import dirname, realpath, join


def iter_tosdr_dataset_texts(type="raw", dataset_filename="tos-dr-5.zip", return_name=False):
    """ Iteration of the input raw texts of the TOSDR-5 dataset.
        type: str
            type of texts to iter from TOS-DR5 dataset.
    """
    assert(isinstance(type, str) and type in ["raw", "summ"])

    dir_path = dirname(realpath(__file__))
    dataset_path = join(dir_path, "../../data/", dataset_filename)
    with zipfile.ZipFile(dataset_path, "r") as f:
        for name in f.namelist():
            if "_{}.txt".format(type) not in name:
                continue
            text = f.read(name)

            data = str(text.decode('utf-8'))
            if return_name:
                data = [name, data]

            yield data
