import os
import shutil
import argparse

from pdf_paper_title import get_paper_title


def foreach_files(root_dir):
    filename_list = []
    for root, dirs, files in os.walk(root_dir):
        for filename in files:
            if not str(filename).lower().endswith(".pdf"):
                continue
            filename = os.path.join(root_dir, filename)
            filename_list.append(filename)
    return filename_list


def pdf_paper_rename(filename, output_dir, paper_type="arxiv"):
    # windows不支持的字符
    unsupported_char = "\\/:*?\"<>\|"
    # print(unsupported_char)
    title = get_paper_title(filename)
    # print(title)
    renamed_title = ""
    for c in title:
        if c in unsupported_char:
            renamed_title += "_"
        else:
            renamed_title += c

    if str(paper_type).lower() == "arxiv":
        output_filename = "{}-{}".format(renamed_title, os.path.basename(filename))
    else:
        output_filename = "{}.pdf".format(renamed_title)

    output_filename = os.path.join(output_dir, output_filename)
    shutil.copy(filename, output_filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, default="./data", help="path to pdf data dir")
    parser.add_argument("--output_dir", type=str, default="./output", help="path to output dir")
    parser.add_argument("--is_arxiv", action="store_true", help="is arxiv pdf paper")
    args = parser.parse_args()

    root_dir = args.data_dir
    output_dir = args.output_dir

    os.makedirs(output_dir, exist_ok=True)

    if args.is_arxiv:
        paper_type = "arxiv"
    else:
        paper_type = None

    filename_list = foreach_files(root_dir)
    for filename in filename_list:
        pdf_paper_rename(filename, output_dir, paper_type)
