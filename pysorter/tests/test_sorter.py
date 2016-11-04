@helper.tempdir
def preparefiles(self):
    with TempDirectory() as d:
        filetypes = {
            r'\.pdf$': 'docs/'
        }
        to_sort = "sourcefiles/"
        to_make = ["file1.pdf", ]

        helper.initialize_dir(d, filetypes, helper.build_path_tree(to_make, to_sort))
        sort = d.path + "/sourcefiles/"
        args = [sort,'-rn']
        pysorter.main(args)
        return d.path


def test_print_changes(capsys):
    p = preparefiles()
    out, err = capsys.readouterr()
    assert out == "move file file1.pdf --> "+p+"/sourcefiles/documents/pdf/file1.pdf\n"
