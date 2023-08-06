import os
from glob import glob
import time
import re
import nibabel as nib
import pandas as pd
from medpy.metric.binary import dc
import numpy as np
import sys

class Metrics():
    def __init__(self,):
        self.header = ["Name", "Dice LV", "Volume LV", "Err LV(ml)",
                        "Dice RV", "Volume RV", "Err RV(ml)",
                        "Dice MYO", "Volume MYO", "Err MYO(ml)"]

    def conv_int(self, i):
        return int(i) if i.isdigit() else i

    def natural_order(self, sord):
        if isinstance(sord, tuple):
            sord = sord[0]
        return [self.conv_int(c) for c in re.split(r'(\d+)', sord)]

    def load_nii(self, img_path):
        nimg = nib.load(img_path)
        return nimg.get_data(), nimg.affine, nimg.header

    def metrics(self, img_gt, img_pred, voxel_size):
        if img_gt.ndim != img_pred.ndim:
            raise ValueError("The arrays 'img_gt' and 'img_pred' should have the "
                             "same dimension, {} against {}".format(img_gt.ndim,
                                                                    img_pred.ndim))
        res = []
        for c in [3, 1, 2]:
            gt_c_i = np.copy(img_gt)
            gt_c_i[gt_c_i != c] = 0
            pred_c_i = np.copy(img_pred)
            pred_c_i[pred_c_i != c] = 0
            gt_c_i = np.clip(gt_c_i, 0, 1)
            pred_c_i = np.clip(pred_c_i, 0, 1)
            dice = dc(gt_c_i, pred_c_i)
            volpred = pred_c_i.sum() * np.prod(voxel_size) / 1000.
            volgt = gt_c_i.sum() * np.prod(voxel_size) / 1000.
            res += [dice, volpred, volpred-volgt]
        return res
        
    def metrics_on_files(self, path_gt, path_pred):
        gt, _, header = self.load_nii(path_gt)
        pred, _, _ = self.load_nii(path_pred)
        zooms = header.get_zooms()
        name = os.path.basename(path_gt)
        name = name.split('.')[0]
        res = self.metrics(gt, pred, zooms)
        res = ["{:.3f}".format(r) for r in res]
        formatting = "{:>14}, {:>7}, {:>9}, {:>10}, {:>7}, {:>9}, {:>10}, {:>8}, {:>10}, {:>11}"
        print(formatting.format(*self.header))
        print(formatting.format(name, *res))

    def metrics_on_dir(self, dir_gt, dir_pred):
        lst_gt = sorted(glob(os.path.join(dir_gt, '*')), key = self.natural_order)
        lst_pred = sorted(glob(os.path.join(dir_pred, '*')), key = self.natural_order)
        res = []
        for p_gt, p_pred in zip(lst_gt, lst_pred):
            if os.path.basename(p_gt) != os.path.basename(p_pred):
                raise ValueError("The two files don't have the same name"
                                 " {}, {}.".format(os.path.basename(p_gt),
                                                   os.path.basename(p_pred)))
            gt, _, header = self.load_nii(p_gt)
            pred, _, _ = self.load_nii(p_pred)
            zooms = header.get_zooms()
            res.append(self.metrics(gt, pred, zooms))
        lst_name_gt = [os.path.basename(gt).split(".")[0] for gt in lst_gt]
        res = [[n,] + r for r, n in zip(res, lst_name_gt)]
        df = pd.DataFrame(res, columns = self.header)
        df.to_csv("results_{}.csv".format(time.strftime("%Y%m%d_%H%M%S")), index=False)


if __name__ == "__main__":
    metric = Metrics()
    metric.metrics_on_files(sys.argv[1], sys.argv[2])
