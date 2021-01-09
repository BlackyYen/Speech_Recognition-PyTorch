import fnmatch
import os
import librosa
import numpy as np
from torch.utils.data import Dataset
from torch.utils.data import DataLoader


class Aduio_DataLoader(Dataset):
    def __init__(self, data_folder, sr=16000, dimension=8192):
        self.data_folder = data_folder
        self.sr = sr
        self.dim = dimension

        # 獲取音訊名列表
        self.wav_list = []
        for root, dirnames, filenames in os.walk(data_folder):
            for filename in fnmatch.filter(
                    filenames, "*.wav"):  # 實現列表特殊字元的過濾或篩選,返回符合匹配「.wav」字元列表
                self.wav_list.append(os.path.join(root, filename))

    def __getitem__(self, item):
        # 讀取一個音訊檔，返回每個音訊資料
        filename = self.wav_list[item]
        # print(filename)
        wb_wav, _ = librosa.load(filename, sr=self.sr)

        # 取幀
        if len(wb_wav) >= self.dim:
            max_audio_start = len(wb_wav) - self.dim
            audio_start = np.random.randint(0, max_audio_start)
            wb_wav = wb_wav[audio_start:audio_start + self.dim]
        else:
            wb_wav = np.pad(wb_wav, (0, self.dim - len(wb_wav)), "constant")

        return wb_wav, filename

    def __len__(self):
        # 音訊檔的總數
        return len(self.wav_list)


# train_set = Aduio_DataLoader(
#     r'D:\dataset\ntut-ml-2020-spring-taiwanese-e2e\train', sr=16000)
# train_loader = DataLoader(train_set, batch_size=8, shuffle=True)

# for (i, data) in enumerate(train_loader):
#     wav_data, wav_name = data
#     print(wav_data.shape)  # torch.Size([8, 8192])
