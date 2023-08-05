#!/bin/env python

import json
import shlex
import subprocess
import sys

from pathlib import Path
from subprocess import PIPE, STDOUT

import numpy as np
from math import log10, ceil, floor
from math import log as ln

import matplotlib
from matplotlib import pyplot as plt

from Av1an.bar import process_pipe
from Chunks.chunk import Chunk

matplotlib.use('Agg')


def read_json(file):
    """
    Reads file and return dictionary of it's contents

    :return: Vmaf file dictionary
    :rtype: dict
    """
    with open(file, 'r') as f:
        fl = json.load(f)
        return fl


def call_vmaf(chunk: Chunk, encoded: Path, n_threads, model, res,
              fl_path: Path = None, vmaf_filter=None, vmaf_rate=0):
    cmd = ''

    # settings model path
    mod = f":model_path={model}" if model else ''

    # limiting amount of threads for calculation
    n_threads = f':n_threads={n_threads}' if n_threads else ''

    if fl_path is None:
        fl_path = chunk.fake_input_path.with_name(encoded.stem).with_suffix('.json')
    fl = fl_path.as_posix()

    filter = vmaf_filter + ',' if vmaf_filter else ''

    # For vmaf calculation both source and encoded segment scaled to 1080
    # Also it's required to use -r before both files of vmaf calculation to avoid errors

    cmd_in = ('ffmpeg', '-loglevel', 'info', '-y', '-thread_queue_size', '1024', '-hide_banner',
              '-r', '60', '-i', encoded.as_posix(), '-r', '60', '-i', '-')

    filter_complex = ('-filter_complex',)

    # Change framerate of comparison to framerate of probe
    select_frames = f"select=not(mod(n\\,{vmaf_rate}))," if vmaf_rate != 0 else ''

    distorted = f'[0:v]{select_frames}scale={res}:flags=bicubic:force_original_aspect_ratio=decrease,setpts=PTS-STARTPTS[distorted];'

    ref = fr'[1:v]{select_frames}{filter}scale={res}:flags=bicubic:force_original_aspect_ratio=decrease,setpts=PTS-STARTPTS[ref];'

    vmaf_filter = f"[distorted][ref]libvmaf=log_fmt='json':eof_action=endall:log_path={shlex.quote(fl)}{mod}{n_threads}"

    cmd_out = ('-f', 'null', '-')

    cmd = (*cmd_in, *filter_complex, distorted + ref + vmaf_filter, *cmd_out)

    ffmpeg_gen_pipe = subprocess.Popen(chunk.ffmpeg_gen_cmd, stdout=PIPE, stderr=STDOUT)
    pipe = subprocess.Popen(cmd, stdin=ffmpeg_gen_pipe.stdout,
                            stdout=PIPE, stderr=STDOUT, universal_newlines=True)
    process_pipe(pipe, chunk)

    return fl_path


def get_percentile(scores, percent):
    """
    Find the percentile of a list of values.
    :param scores: - is a list of values. Note N MUST BE already sorted.
    :param percent: - a float value from 0.0 to 1.0.
    :return: - the percentile of the values
    """
    scores = sorted(scores)
    key = lambda x: x

    k = (len(scores)-1) * percent
    f = floor(k)
    c = ceil(k)
    if f == c:
        return key(scores[int(k)])

    d0 = (scores[int(f)]) * (c-k)
    d1 = (scores[int(c)]) * (k-f)
    return d0+d1


def transform_vmaf(vmaf):
    if vmaf<99.99:
        return -ln(1-vmaf/100)
    else:
        # return -ln(1-99.99/100)
        return 9.210340371976184


def read_weighted_vmaf(file, percentile=0):
    """Reads vmaf file with vmaf scores in it and return N percentile score from it.

    :return: N percentile score
    :rtype: float
    """

    jsn = read_json(file)

    vmafs = sorted([x['metrics']['vmaf'] for x in jsn['frames']])

    percentile = percentile if percentile != 0 else 0.25
    score = get_percentile(vmafs, percentile)

    return round(score, 2)


def plot_vmaf(source: Path, encoded: Path, args, model, vmaf_res):
    """
    Making VMAF plot after encode is done
    """

    print('Calculating Vmaf...\r', end='')


    fl_path = encoded.with_name(f'{encoded.stem}_vmaflog').with_suffix(".json")

    # call_vmaf takes a chunk, so make a chunk of the entire source
    ffmpeg_gen_cmd = ['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-i',
                      source.as_posix(), *args.pix_format, '-f', 'yuv4mpegpipe', '-']
    input_chunk = Chunk(args.temp, 0, ffmpeg_gen_cmd, '', 0, 0)

    scores = call_vmaf(input_chunk, encoded, 0, model, vmaf_res, fl_path=fl_path)

    if not scores.exists():
        print(f'Vmaf calculation failed for chunks:\n {source.name} {encoded.stem}')
        sys.exit()

    file_path = encoded.with_name(f'{encoded.stem}_plot').with_suffix('.png')
    plot_vmaf_score_file(scores, file_path)


def plot_vmaf_score_file(scores: Path, plot_path: Path):
    """
    Read vmaf json and plot VMAF values for each frame
    """

    perc_1 = read_weighted_vmaf(scores, 0.01)
    perc_25 = read_weighted_vmaf(scores, 0.25)
    perc_75 = read_weighted_vmaf(scores, 0.75)
    mean = read_weighted_vmaf(scores, 0.50)

    with open(scores) as f:
        file = json.load(f)
        vmafs = [x['metrics']['vmaf'] for x in file['frames']]
        plot_size = len(vmafs)

    figure_width = 3 + round((4 * log10(plot_size)))
    plt.figure(figsize=(figure_width, 5))

    plt.plot([1, plot_size], [perc_1, perc_1], '-', color='red')
    plt.annotate(f'1%: {perc_1}', xy=(0, perc_1), color='red')

    plt.plot([1, plot_size], [perc_25, perc_25], ':', color='orange')
    plt.annotate(f'25%: {perc_25}', xy=(0, perc_25), color='orange')

    plt.plot([1, plot_size], [perc_75, perc_75], ':', color='green')
    plt.annotate(f'75%: {perc_75}', xy=(0, perc_75), color='green')

    plt.plot([1, plot_size], [mean, mean], ':', color='black')
    plt.annotate(f'Mean: {mean}', xy=(0, mean), color='black')

    for i in range(0, 100):
        plt.axhline(i, color='grey', linewidth=0.4)
        if i % 5 == 0:
            plt.axhline(i, color='black', linewidth=0.6)

    plt.plot(range(plot_size), vmafs,
             label=f'Frames: {plot_size}\nMean:{mean}\n'
                   f'1%: {perc_1} \n25%: {perc_25} \n75%: {perc_75}', linewidth=0.7)
    plt.ylabel('VMAF')
    plt.legend(loc="lower right", markerscale=0, handlelength=0, fancybox=True, )
    plt.ylim(int(perc_1), 100)
    plt.tight_layout()
    plt.margins(0)

    # Save
    plt.savefig(plot_path, dpi=250)
