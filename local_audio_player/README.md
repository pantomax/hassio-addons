### Configuration

usage
```yaml
      - service: hassio.addon_stdin     
        data:        
          addon: local_audio_player #placeholder
          input: "http://localhost:8123/local/song.mp3"
```

Replace `local_audo_player` with the id found in the url of this add on page

e.g. `/hassio/addon/de3cd379_audio_player` means that `local_audio_player` should be changed to `de3cd379_audio_player` 


### Local files
make sure that song.mp3 (or any other files) are located in the ~/config/www/ directory.

### Example script

```yaml
script:
  play_audio:
    sequence:
      - service: hassio.addon_stdin     
        data:        
          addon: # local_audio_player          
          input: "http://localhost:8123/local/song.mp3"
```



