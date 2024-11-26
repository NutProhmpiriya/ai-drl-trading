# AI-DRL Trading

This project is designed to create an AI-based Forex trading system using Deep Reinforcement Learning (DRL) on MetaTrader 5 (MT5). The following describes the folder structure and the purpose of each folder and file in the project.

## Folder Structure

```
## Folder Structure

/forex_ai_trader
│
├── /data
│   └── /raw                    # ข้อมูลดิบจาก MT5 (ราคาคู่เงิน)
│
├── /env                        # Environment สำหรับ DRL เชื่อมต่อ MT5
│   └── mt5_env.py              # คลาสที่เชื่อมต่อกับ MT5
│
├── /models                     # โมเดลที่ฝึกแล้ว
│   └── /dqn                    # โมเดล DQN
│
├── /scripts                    # สคริปต์หลักสำหรับการฝึกและทดสอบโมเดล
│   ├── /train_model.py          # ฝึกโมเดล DRL
│   └── /trade.py                # ใช้โมเดลในการเทรดจริง
│
├── /config                     # คอนฟิกูเรชันพื้นฐาน
│   └── settings.py             # ค่าคอนฟิกูเรชัน MT5, AI
│
├── requirements.txt            # รายการไลบรารีที่ต้องใช้
└── README.md                   # ข้อมูลเบื้องต้น


```

## Description of Folders and Files

### `/etc`

This folder contains configuration files for the project. These files specify various settings for the DRL model, such as hyperparameters, MT5 connection configurations, and other environment settings.

- `settings.py`: This file includes the configuration for MT5, the DRL model, and any hyperparameters required for training and testing.

### `/include`

This folder contains any necessary include files, such as header files for external dependencies or reusable components. It might include files for shared functions or data processing.

- Example: `some_header.h` (if necessary for a specific dependency or module).

### `/lib`

This folder contains external libraries that the project depends on. These could be either custom or third-party libraries that extend the functionality of the project.

- Example: `external_lib.py` could include a library used to fetch data from an external source or to handle specialized calculations.

### `/scripts`

The `scripts` folder contains the core Python scripts used for training, testing, and deploying the DRL model. These scripts are essential for running the project and interacting with the MetaTrader 5 platform.

- `train_model.py`: This script is used to train the DRL model. It processes the data, sets up the training environment, and initiates the training process.
- `backtest.py`: This script allows you to backtest the trained model against historical market data to evaluate its performance.
- `trade.py`: This script interacts with MetaTrader 5 (MT5) for live trading. It uses the trained model to make trading decisions in real-time based on market data.

### `/share`

This folder contains shared resources that are used across multiple scripts or by different parts of the project. These include saved models, logs, and datasets.

- `logs/`: This subfolder contains log files that record trading actions, system errors, or performance metrics.
- `models/`: This subfolder contains the pre-trained models or model checkpoints that can be loaded for further training or live trading.

### `.gitignore`

This file specifies which files and folders should be ignored by Git. For example, it excludes virtual environments, IDE-specific files, and other generated files that are not needed in version control.

### `pyvenv.cfg`

This configuration file is used to store settings related to the virtual environment used for the project. It helps track the Python environment configuration.

### `requirements.txt`

This file lists all the necessary Python libraries and dependencies for the project. You can install the dependencies using the following command:

```bash
pip install -r requirements.txt
```
