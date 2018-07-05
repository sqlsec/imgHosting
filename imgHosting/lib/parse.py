# coding: utf-8
import optparse

def create_cmd_parser():
    usage = "'python3 %prog -f|--filename <filename> -h help'"
    parser = optparse.OptionParser(usage)
    parser.add_option("-f", "--filename", dest="filename", help="指定上传的图片(或gif等)")
    (options,args) = parser.parse_args()
    if options.filename == None:
        parser.error("需要参数filename; -f|--filename <filename>")
    return options