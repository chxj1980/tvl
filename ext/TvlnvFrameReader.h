#pragma once

#include <cuda.h>

#include "NvDecoder/NvDecoder.h"
#include "Utils/FFmpegDemuxer.h"

#include "MemManager.h"

class TvlnvFrameReader
{
public:
    TvlnvFrameReader(MemManager* mem_manager, std::string video_file_path, int gpu_index, Rect* crop_rect=NULL, Dim* resize_dim=NULL);
    ~TvlnvFrameReader();

    std::string get_filename();
    int get_width();
    int get_height();
    int get_frame_size();
    void seek(float time_secs);
    uint8_t* read_frame();

private:
    MemManager* _mem_manager;
    std::string _filename;
    CUcontext _cu_context = NULL;
    FFmpegDemuxer* _demuxer;
    NvDecoder* _decoder;
};