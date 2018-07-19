import csv

import fire

from . import api


def download_entries(path, start_id, end_id, verbose=True):
    """ start_id - end_id arasi (start_id dahil, end_id haric) entry
    numarasina sahip entry'leri path adresindeki dosyaya yazar"""
    file_mode = 'w' if start_id == 1 else 'a'
    total = end_id - start_id

    with open(path, file_mode) as output:
        writer = csv.DictWriter(
            output, fieldnames=['id', 'owner', 'topic', 'body', 'date', 'fav'])
        if file_mode == "w":
            writer.writeheader()

        for id in range(start_id, end_id):
            try:
                entry = api.get_entry_by_id(id)
            except KeyboardInterrupt:
                break
            except:
                print(f"Error at {id}")
                download_entries(path, id, end_id)
                exit()
            if entry:
                writer.writerow(entry)
            if verbose:
                percentage = f"{(100 * (id + 1 - start_id) / total):.2f}"
                print(
                    f"\r[%{percentage}][{id + 1: >9}/{end_id: <9}]",
                    end='',
                    flush=True
                )


if __name__ == '__main__':
    fire.Fire()
