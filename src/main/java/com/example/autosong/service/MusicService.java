package com.example.autosong.service;

import jakarta.annotation.PostConstruct;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.util.LinkedList;
import java.util.List;

@Service
public class MusicService {

    private final List<String> playlist = new LinkedList<>();
    private volatile String nowPlaying = null;

    public String getNowPlaying() {
        return nowPlaying;
    }

    public List<String> getPlaylist() {
        synchronized (playlist) {
            return new LinkedList<>(playlist);
        }
    }

    public void queueSong(String songName) {
        synchronized (playlist) {
            playlist.add(songName);
        }
    }

    @PostConstruct
    public void startPlayer() {
        Thread playerThread = new Thread(() -> {
            while (true) {
                String song = null;
                synchronized (playlist) {
                    if (!playlist.isEmpty()) {
                        song = playlist.remove(0);
                        nowPlaying = song;
                    }
                }

                if (song != null) {
                    playSong(song);
                    nowPlaying = null;
                } else {
                    try {
                        Thread.sleep(1000);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            }
        });

        playerThread.setDaemon(true);
        playerThread.start();
    }

    private void playSong(String songName) {
        System.out.println("🎵 播放中: " + songName);

        try {
            ProcessBuilder pb = new ProcessBuilder(
                    "cmd.exe", "/c", "python", "C:\\Users\\86156\\Desktop\\Program\\python_work\\练习\\auto_music.py", songName
            );
            pb.inheritIO();
            Process process = pb.start();
            process.waitFor();
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }

        System.out.println("✅ 播放完成: " + songName);
    }
}