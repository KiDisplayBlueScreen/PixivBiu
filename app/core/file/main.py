# coding=utf-8
# pylint: disable=relative-beyond-top-level
from ...platform import CMDProcessor
from PIL import Image
import zipfile
import json
import yaml
import os


@CMDProcessor.core_register("file")
class core_module_file(object):
    def __init__(self):
        pass

    def ain(self, uri, mode="r"):
        if not os.path.exists(uri):
            return False
        try:
            with open(uri, mode) as f:
                fileType = uri.split(".")[-1]
                if fileType == "json":
                    f = json.load(f)
                elif fileType == "yml" or fileType == "yaml":
                    f = yaml.safe_load(f)
        except:
            return False
        return f

    def aout(self, uri, data, mode="w"):
        if not uri:
            return False

        uri = uri.replace("\\\\", "/").replace("\\", "/").replace("//", "/")
        uriDir = ""
        for x in uri.split("/")[:-1]:
            uriDir = uriDir + x + "/"
        fileType = uri.split(".")[-1]
        if uriDir != "" and not os.path.exists(uriDir):
            os.makedirs(uriDir)
        try:
            with open(uri, mode) as f:
                if fileType == "json":
                    data = json.dumps(data)
                elif fileType == "yml" or fileType == "yaml":
                    data = yaml.dump(data)
                f.write(data)
        except:
            return False
        print(
            "\033[32m[saved]\033[0m \033[36m%s\033[0m -> \033[36m%s\033[0m"
            % (uri.split("/")[-1], uri)
        )
        return True

    def unzip(self, ruri, furi):
        try:
            f = zipfile.ZipFile(furi, "r")
            for name in f.namelist():
                f.extract(name, ruri)
            f.close()
        except:
            return False
        return True

    def cov2webp(self, uri, plist, dlist, quality=100):
        imgs = []
        try:
            for x in plist:
                imgs.append(Image.open(x))
            imgs[0].save(
                uri,
                "webp",
                quality=quality,
                save_all=True,
                append_images=imgs[1:],
                duration=dlist,
            )
        except:
            return False
        return True

    def cov2gif(self, uri, plist, dlist):
        imgs = []
        try:
            for x in plist:
                imgs.append(Image.open(x))
            imgs[0].save(
                uri,
                "gif",
                save_all=True,
                append_images=imgs[1:],
                duration=dlist,
                loop=0
            )
        except:
            return False
        return True