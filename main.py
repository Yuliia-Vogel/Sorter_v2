import sys
import os
import shutil

import normalization
import del_empty_dirs


def main():
    lenargv = len(sys.argv)  # sys.argv - через нього отримуємо шлях до папки, яку треба опрацювати
    if lenargv != 2:  # перевіряємо довжину аргумента: [0]назва файлу sort.py і [1]шлях до папки
        print("Incorrect number of arguments! exit1")
        exit(1)
    elif lenargv == 2:
        print('Agrv is Ok')
        path = sys.argv[1]
        if os.path.isfile(path):  # перевірка, чи шлях є папкою, якщо не папка - то екзіт
            print("this is file, cannot work with it, exit")
            exit(1)
        elif os.path.isdir(path):
            print("this is folder, I go to work with it")
            folder_processing(path)  # тут виклик функції обробки папки, бо все з посиланням на папку Ок
        else:
            print("file type is different, cannot work with it, exit")


ignore_list = {'images', 'documents', 'audio', 'video', 'archives', 'others', 'no_extension'}

images_list = []
documents_list = []
audio_list = []
video_list = []
archives_list = []
no_extension_list = []
others_list = []

types_set = set()
unknown_types_set = set()


def folder_processing(path):
    for root, dirs, files in os.walk(path, topdown=True):
        dirs[:] = [d for d in dirs if d not in ignore_list]
        for file in files:
            file_path = os.path.join(root, file)

            if os.path.isfile(file_path):
                filename, file_extension = os.path.splitext(file_path)
                basename = filename.split(os.sep)[-1]

                if file_extension.lower() in ('.jpeg', '.png', '.jpg', '.svg'):
                    types_set.add(file_extension)
                    new_norm_name = file_processing(basename, file_extension, path, file_path, "images")
                    images_list.append(new_norm_name)

                elif file_extension.lower() in ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'):
                    types_set.add(file_extension)
                    new_norm_name = file_processing(basename, file_extension, path, file_path, "documents")
                    documents_list.append(new_norm_name)

                elif file_extension.lower() in ('.mp3', '.ogg', '.wav', '.amr'):
                    types_set.add(file_extension)
                    new_norm_name = file_processing(basename, file_extension, path, file_path, "audio")
                    audio_list.append(new_norm_name)

                elif file_extension.lower() in ('.avi', '.mp4', '.mov', '.mkv'):
                    types_set.add(file_extension)
                    new_norm_name = file_processing(basename, file_extension, path, file_path, "video")
                    video_list.append(new_norm_name)

                elif file_extension.lower() in ('.zip', '.gz', '.tar'):
                    types_set.add(file_extension)
                    new_norm_name = file_processing(basename, file_extension, path, file_path, "archives", True)
                    archives_list.append(new_norm_name)

                elif file_extension == '':
                    unknown_types_set.add(file_extension)
                    new_norm_name = file_processing(basename, file_extension, path, file_path, "no_extension")
                    no_extension_list.append(new_norm_name)

                else:
                    new_norm_name = file_processing(basename, file_extension, path, file_path, "others")
                    others_list.append(new_norm_name)
                    unknown_types_set.add(file_extension)

    del_empty_dirs.remove_empty_folders(path)

    print(images_list)
    print(documents_list)
    print(audio_list)
    print(video_list)
    print(archives_list)
    print(no_extension_list)
    print(others_list)

    print(types_set)
    print(unknown_types_set)


def file_processing(basename, file_extension, path, file_path, foldername, archive=False):
    new_norm_name = ''
    with_end = ''
    try:
        dir_path = os.path.join(path, foldername)  # створення шляху папки
        os.mkdir(dir_path)  # створення папки
    except FileExistsError:  # якщо папка вже існує
        pass
    norm_name = normalization.normalize(basename, file_extension)
    new_file_path = os.path.join(dir_path, norm_name)
    dup = 0
    while os.path.isfile(new_file_path):  # перевіряю, чи такий файл уже існує
        dup += 1
        new_dup_name = f"{basename}_{dup}"
        with_end = f'{new_dup_name}{file_extension}'
        new_file_path = (os.path.join(dir_path, with_end))
    if archive:
        try:
            file_a, _ = os.path.splitext(new_file_path)
            shutil.unpack_archive(file_path, file_a)
            os.remove(file_path)
        except shutil.ReadError:
            shutil.move(file_path, new_file_path)
    else:
        shutil.move(file_path, new_file_path)
    if with_end:
        new_norm_name += with_end
    else:
        new_norm_name += norm_name

    return new_norm_name






if __name__ == '__main__':
    # sys.argv[1] - другий переданий через консоль аргумент - це папка, яку треба опрацювати
    main()


