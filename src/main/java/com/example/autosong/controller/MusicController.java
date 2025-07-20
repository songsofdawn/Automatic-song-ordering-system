package com.example.autosong.controller;

import com.example.autosong.service.MusicService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.*;

@RestController
@RequestMapping("/api")
public class MusicController {

    @Autowired
    private MusicService musicService;

    @PostMapping("/queue")
    public Map<String, String> queueSong(@RequestBody Map<String, String> body) {
        String song = body.get("song");
        if (song == null || song.trim().isEmpty()) {
            return Map.of("status", "error", "message", "请输入歌名");
        }
        musicService.queueSong(song.trim());
        return Map.of("status", "ok", "message", "已加入播放列表");
    }

    @GetMapping("/playlist")
    public Map<String, Object> getPlaylist() {
        return Map.of(
                "nowPlaying", musicService.getNowPlaying(),
                "playlist", musicService.getPlaylist()
        );
    }
}
