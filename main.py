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

ignore_list = set(['images', 'documents', 'audio', 'video', 'archives', 'others', 'no_extension', 'empty_archives'])

images_list = []
documents_list = []
audio_list = []
video_list = []
archives_list = []
empty_archives = []
no_extension_list = []
others_list = []

types_set = set()
unknown_types_set = set()


def folder_processing(path):
    for root, dirs, files in os.walk(path, topdown=True):
        dirs[:] = [d for d in dirs if d not in ignore_list]
        for file in files:
            file_path = os.path.join(root, file)
            print(file)
            if os.path.isfile(file_path):
                filename, file_extension = os.path.splitext(file_path)
                file_extention1 = file_extension
                basename = filename.split(os.sep)[-1]

                if file_extension in ('.jpeg', '.png', '.jpg', '.svg'):
                    types_set.add(file_extention1)
                    new_norm_name = file_processing(basename, file_extention1, path, file_path, "images")
                    images_list.append(new_norm_name)

                elif file_extension in ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'):
                    types_set.add(file_extention1)
                    new_norm_name = file_processing(basename, file_extention1, path, file_path, "documents")
                    documents_list.append(new_norm_name)

                elif file_extension in ('.mp3', '.ogg', '.wav', '.amr'):
                    types_set.add(file_extention1)
                    new_norm_name = file_processing(basename, file_extention1, path, file_path, "audio")
                    audio_list.append(new_norm_name)

                elif file_extension in ('.avi', '.mp4', '.mov', '.mkv'):
                    types_set.add(file_extention1)
                    new_norm_name = file_processing(basename, file_extention1, path, file_path, "video")
                    video_list.append(new_norm_name)

                elif file_extension in ('.zip', '.gz', '.tar'):
                    types_set.add(file_extention1)
                    try:
                        new_norm_name = file_processing(basename, file_extention1, path, file_path, "archives", archive = True)
                        archives_list.append(new_norm_name)
                    except shutil.ReadError:
                        new_norm_name = file_processing(basename, file_extention1, path, file_path, "empty_archives")
                        empty_archives.append(new_norm_name)

                elif file_extension == '':
                    unknown_types_set.add(file_extention1)
                    new_norm_name = file_processing(basename, file_extention1, path, file_path, "no_extension")
                    no_extension_list.append(new_norm_name)

                else:
                    new_norm_name = file_processing(basename, file_extention1, path, file_path, "others")
                    others_list.append(new_norm_name)
                    unknown_types_set.add(file_extention1)

    del_empty_dirs.remove_empty_folders(path)

    print(images_list)
    print(documents_list)
    print(audio_list)
    print(video_list)
    print(archives_list)
    print(empty_archives)
    print(no_extension_list)
    print(others_list)

    print(types_set)




def file_processing(basename, file_extention1, path, file_path, foldername, archive = False):
    new_norm_name = ''
    try:
        dir_path = os.path.join(path, foldername)  # створення шляху папки
        os.mkdir(dir_path)  # створення папки
    except FileExistsError:  # якщо папка вже існує
        pass
    norm_name = normalization.normalize(basename, file_extention1)
    new_file_path = os.path.join(dir_path, norm_name)
    dup = 0
    while os.path.isfile(new_file_path):  # перевіряю, чи такий файл уже існує
        dup += 1
        new_n = f"{basename}_{dup}"
        with_end = f'{new_n}{file_extention1}'
        new_file_path = (os.path.join(dir_path, with_end))
    if archive == True:
        shutil.unpack_archive(file_path, new_file_path)
        os.remove(file_path)
    else:
        shutil.move(file_path, new_file_path)
    new_norm_name += norm_name

    return new_norm_name






if __name__ == '__main__':
    # sys.argv[1] - другий переданий через консоль аргумент - це папку, яку треба опрацювати
    main()


