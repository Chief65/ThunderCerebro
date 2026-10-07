$script = @"
ls -lh
ls -lh .cache
ls -lh cache
ls -lh config
ls -lh libraries
ls -lh versions
ls -lh world/entities
ls -lh world/poi
ls -lh world_nether/DIM-1
ls -lh world_nether/DIM-1/region
ls -lh world_the_end/DIM1
ls -lh world_the_end/DIM1/region
ls -lh Dungeons/region
bye
"@
$script | Out-File -FilePath "C:\Users\PC\Desktop\ThunderCerebro\sftp_scan_dirs.txt" -Encoding utf8
