## Description

Command line input to view or sync missing files in left or right folder.

## Starting
1. Docker
   1. In running container terminal input `fs --help`
   2. Example folders in `FastSync/tests/test_folders/`
   3. Example command `-l "tests/fixtures/test_folders/Simple1" -r "tests/fixtures/test_folders/Simple2" -g missing right`

## Features


- View missing files - [Example](#view-missing-files), [Help](#help-view-missing-files)
- Synchronizing missing files - [Example](#synchronizing-missing-files), [Help](#help-synchronizing-missing-files)
- Content filtering - [Example](#content-filtering)
    - By file extensions
    - By folder names
- Output format
    - By default, (in disarray)
    - Grouping by folders
    - Filtered files

## Help structure


### Main help

```
Usage: fast_sync.py [OPTIONS] COMMAND [ARGS]...

Options:
  -left, -l, --left-folder DIRECTORY
                                  [required]
  -right, -r, --right-folder DIRECTORY
                                  [required]
  -g, --group                     Group files by folders [Affects the output
                                  format]
  -s, --sort                      Sort files by name [Affects the output
                                  format]
  -e, --extensions TEXT           Filter files by extension
  -f, --folders TEXT              Exclude files based on folder
  --help                          Show this message and exit.

Commands:
  missing  View missing files in chosen folder
  sync     Sync chosen folder

```

### Help view missing files

```
Usage: fast_sync.py missing [OPTIONS] COMMAND [ARGS]...

  View missing files in chosen folder

Options:
  --help  Show this message and exit.

Commands:
  left   Missing files in left folder
  right  Missing files in right folder
```

### Help synchronizing missing files

```
Usage: fast_sync.py sync [OPTIONS] COMMAND [ARGS]...

  Sync chosen folder

Options:
  --help  Show this message and exit.

Commands:
  left   Sync left folder with right folder
  right  Sync right folder with left folder
```

```
Usage: fast_sync.py -l sync left [OPTIONS]

Options:
  --view-missing      View missing files
  --check-sync        Check sync status
  --open-sync-folder  Open left folder in file manager
  --help              Show this message and exit.
```


## Examples

Structure example with missing folders, files
```
Folder1                         Folder2
────────────────                ────────────────
📁 Neuropunk                   📁 Neuropunk
├── 📄 Neuropunk - pt. 54.mp3  ├── 📄 Neuropunk - pt. 54.mp3
├── 📄 Neuropunk - pt. 55.mp3  ├── 📄 Neuropunk - pt. 55.mp3
└── ❌ MISSING                 └── 📄 Neuropunk - pt. 55 2.mp3

📁 Rus dnb                     📁 Rus dnb
├── 📄 Dimension - Altar.mp3   ├── 📄 Dimension - Altar.mp3
├── 📄 Drummatix.mp3           ├── 📄 Drummatix.mp3   
├── 📄 Receptor - Samara.mp3   ├── ❌ MISSING  
└── 📄 Receptor - Пантера.mp3  └── ❌ MISSING  

❌ MISSING                     📁 New vegas
```

### View missing files

#### Default output for `Folder1`

**Command**:

```
uv run fast_sync.py -l "/home/puzer/OS_emulate/Folder1" -r "/home/puzer/OS_emulate/Folder2" missing left
```

**Output**:

```
Creating hash: /home/puzer/OS_emulate/Folder1: 6it [00:00, 30.13it/s]
Creating hash: /home/puzer/OS_emulate/Folder2: 9it [00:00, 42.22it/s]
------------------------------------------------------------------------------------------
📊  Total missing files: 5

🚫  Missing files in Folder1:                                                                                                                                                       
***********************************
Bert Weedon - Roundhouse Rock.mp3
Danny Kaye - It's a Sin to Tell a Lie.mp3
Neuropunk - pt. 55 2.mp3
Bert Weedon - Happy Times.mp3
Eddy Arnold - It's a Sin.mp3
***********************************
```

---

#### Grouped output for `Folder2`

**Command** with `-g` (grouped output) option:

```
uv run fast_sync.py -l "/home/puzer/OS_emulate/Folder1" -r "/home/puzer/OS_emulate/Folder2" -g missing right
```

**Output**:

```
Creating hash: /home/puzer/OS_emulate/Folder1: 6it [00:00, 31.02it/s]
Creating hash: /home/puzer/OS_emulate/Folder2: 9it [00:00, 41.62it/s]
------------------------------------------------------------------------------------------
📊  Total missing files: 2

🚫  Missing files in Folder2:                                                                                                                                                       
┌────────────────────────────────────────────────────────────────────────────────────────────────────
├── 📁 Rus dnb/
│   ├── 📄 Receptor - Samara.mp3
│   └── 📄 Receptor - Пантера.mp3
└────────────────────────────────────────────────────────────────────────────────────────────────────
```

### Synchronizing missing files


**Command** for `Folder1` with `--view-missing` and `--check-sync` options:

```
uv run fast_sync.py -l "/home/puzer/OS_emulate/Folder1" -r "/home/puzer/OS_emulate/Folder2" -g sync left --view-missing --check-sync
```

**Output**:
```
Creating hash: /home/puzer/OS_emulate/Folder1: 6it [00:00, 29.91it/s]
Creating hash: /home/puzer/OS_emulate/Folder2: 9it [00:00, 42.38it/s]
------------------------------------------------------------------------------------------
📊  Total missing files: 5

🚫  Missing files in Folder1:                                                                                                                                                 
┌─────────────────────────────────────────────────────────────────────────
├── 📁 Neuropunk/
│   └── 📄 Neuropunk - pt. 55 2.mp3
├── 📁 New vegas/
│   ├── 📄 Bert Weedon - Happy Times.mp3
│   ├── 📄 Bert Weedon - Roundhouse Rock.mp3
│   ├── 📄 Danny Kaye - It's a Sin to Tell a Lie.mp3
│   └── 📄 Eddy Arnold - It's a Sin.mp3
└─────────────────────────────────────────────────────────────────────────
Are you sure you want to sync Folder1 with Folder2? [y/N]: y

🔄  Syncing folders: Folder2  ⟹  Folder1                                                                                                                                      
Copying files: 100%|███████████████████████████████████████| 5/5 [00:00<00:00, 90.59file/s]
Successful syncing folders: Folder1 with Folder2

🔁  Repeat check in folder: Folder1                                                                                                                                           
Creating hash: /home/puzer/OS_emulate/Folder1: 11it [00:00, 52.57it/s]
Creating hash: /home/puzer/OS_emulate/Folder2: 9it [00:00, 41.71it/s]

🗹  No missing files found in Folder1       
```

---

**Command** for `Folder2`:


```
uv run fast_sync.py -l "/home/puzer/OS_emulate/Folder1" -r "/home/puzer/OS_emulate/Folder2" -g sync right
```

**Output**:
```
Creating hash: /home/puzer/OS_emulate/Folder1: 11it [00:00, 49.48it/s]
Creating hash: /home/puzer/OS_emulate/Folder2: 9it [00:00, 41.51it/s]
------------------------------------------------------------------------------------------
Are you sure you want to sync Folder2 with Folder1? [y/N]: y

🔄  Syncing folders: Folder1  ⟹  Folder2
Copying files: 100%|██████████████████████████████████████████| 2/2 [00:00<00:00, 166.92file/s]
Successful syncing folders: Folder2 with Folder1
```



### Content filtering

Exclude `New vegas` folder and only files with `.wav` extension. For this example I added file `Rus dnb/Collapse.wav` in `Folder2`

**Command**:
```
uv run fast_sync.py -l "/home/puzer/OS_emulate/Folder1" -r "/home/puzer/OS_emulate/Folder2" -g -e ".wav" -f "New vegas" missing left
```

**Output**:
```
Creating hash: /home/puzer/OS_emulate/Folder1: 0it [00:00, ?it/s]
Creating hash: /home/puzer/OS_emulate/Folder2: 1it [00:00, 14.05it/s]
------------------------------------------------------------------------------------------
📊  Total missing files: 1

🚫  Missing files in Folder1:                                                                                                                                                 
┌──────────────────────────────────────────────────────────────────────────────────────────
├── 📁 Rus dnb/
│   └── 📄 Collapse.wav
└──────────────────────────────────────────────────────────────────────────────────────────
```
