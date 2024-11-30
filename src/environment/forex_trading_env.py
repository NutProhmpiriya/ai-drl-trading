import gymnasium as gym  # ใช้ Gymnasium แทน Gym
import numpy as np
import pandas as pd
import plotly.graph_objects as go

class ForexEnv(gym.Env):
    def __init__(self, data, initial_balance=10000, max_daily_loss=0.01, window_size=50, risk_per_trade=0.01, leverage=50):
        super(ForexEnv, self).__init__()

        # ข้อมูลการเทรด (OHLCV)
        self.data = data
        self.initial_balance = initial_balance
        self.max_daily_loss = max_daily_loss
        self.window_size = window_size
        self.risk_per_trade = risk_per_trade
        self.leverage = leverage  # ใช้ Leverage

        # ตัวแปรการเทรด
        self.current_step = self.window_size
        self.balance = self.initial_balance
        self.daily_loss = 0
        self.position = 0  # 1 = long, -1 = short, 0 = no position
        self.entry_price = 0
        self.stop_loss = 0
        
        # กำหนด Action Space และ Observation Space
        self.action_space = gym.spaces.Discrete(3)  # 0 = Buy, 1 = Hold, 2 = Sell
        self.observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=(self.window_size, 4), dtype=np.float32)

        # เก็บข้อมูลสำหรับการแสดงกราฟ
        self.balance_history = [self.balance]

    def reset(self):
        # รีเซ็ตสถานะทั้งหมดเมื่อเริ่มใหม่
        self.current_step = self.window_size
        self.balance = self.initial_balance
        self.daily_loss = 0
        self.position = 0
        self.entry_price = 0
        self.stop_loss = 0
        self.balance_history = [self.balance]  # เคลียร์ประวัติการ Balance
        return self.get_observation(), {}

    def get_observation(self):
        # คืนค่าข้อมูลปัจจุบัน เช่น Open, High, Low, Close
        obs = np.array([
            self.data.iloc[self.current_step - self.window_size:self.current_step][['Open', 'High', 'Low', 'Close']].values
        ])
        return obs

    def step(self, action):
        # ข้อมูลปัจจุบัน (OHLC)
        high_price = self.data.iloc[self.current_step]['High']
        low_price = self.data.iloc[self.current_step]['Low']

        # ใช้ข้อมูล Spread จากคอลัมน์ `Spread`
        spread = self.data.iloc[self.current_step]['Spread']
        
        # คำนวณราคา Bid และ Ask โดยใช้ Spread
        bid_price = low_price  # ใช้ราคาขาย (Bid) เป็นราคาต่ำสุด (Low)
        ask_price = high_price  # ใช้ราคาซื้อ (Ask) เป็นราคาสูงสุด (High)
        
        reward = 0
        done = False
        
        # คำนวณการขาดทุนสะสมรายวัน
        if self.balance < self.initial_balance * (1 - self.max_daily_loss):
            done = True
            return self.get_observation(), reward, done, {'info': 'Max daily loss reached'}
        
        # การเปิดตำแหน่ง
        if action == 0 and self.position == 0:  # Buy
            position_size = self.calculate_position_size(ask_price)  # ใช้ Ask Price ในการซื้อ
            self.position = 1  # เปิด Long Position
            self.entry_price = ask_price
            self.stop_loss = ask_price * 0.99  # สมมติว่า Stop Loss = 1% ของราคาปัจจุบัน
            self.balance -= position_size * ask_price
            reward = 0
        elif action == 2 and self.position == 0:  # Sell
            position_size = self.calculate_position_size(bid_price)  # ใช้ Bid Price ในการขาย
            self.position = -1  # เปิด Short Position
            self.entry_price = bid_price
            self.stop_loss = bid_price * 1.01  # สมมติว่า Stop Loss = 1% ของราคาปัจจุบัน
            self.balance += position_size * bid_price
            reward = 0
        elif action == 1:  # Hold
            reward = 0
        
        # การปิดตำแหน่ง
        if self.position == 1 and bid_price <= self.stop_loss:  # ใช้ราคาขาย (Bid) ในการปิดตำแหน่ง
            self.balance += self.calculate_position_size(bid_price) * bid_price
            reward = (bid_price - self.entry_price) * self.calculate_position_size(bid_price)
            self.position = 0
        elif self.position == -1 and ask_price >= self.stop_loss:  # ใช้ราคา Ask ในการปิดตำแหน่ง
            self.balance -= self.calculate_position_size(ask_price) * ask_price
            reward = (self.entry_price - ask_price) * self.calculate_position_size(ask_price)
            self.position = 0

        # เก็บข้อมูล Balance สำหรับการแสดงกราฟ
        self.balance_history.append(self.balance)

        # ตรวจสอบว่าเสร็จสิ้นหรือยัง
        self.current_step += 1
        if self.current_step >= len(self.data) - 1:
            done = True

        # แสดงผลกราฟ
        self.render()

        return self.get_observation(), reward, done, {}

    def calculate_position_size(self, current_price):
        # คำนวณขนาดตำแหน่งตามความเสี่ยงที่ต้องการ พร้อมใช้ Leverage
        stop_loss_distance = abs(current_price - self.stop_loss)
        position_size = (self.balance * self.risk_per_trade) / stop_loss_distance
        
        # ใช้ leverage เพื่อขยายขนาดตำแหน่ง
        position_size *= self.leverage
        return position_size

    def render(self):
        # ใช้ Plotly สำหรับการแสดงผลกราฟ
        fig = go.Figure()

        fig.add_trace(go.Scatter(x=list(range(len(self.balance_history))), y=self.balance_history, mode='lines', name='Balance'))

        fig.update_layout(
            title="Balance Over Time",
            xaxis_title="Steps",
            yaxis_title="Balance",
            showlegend=True
        )

        fig.show()

