
class Signal():
    def __init__(self,path,fs,chan, lowfilt, highfilt, transpose):
        self.path = path
        self.fs = fs
        self.chan = chan+2
        self.lowfilt = lowfilt/(fs/2)
        self.highfilt = highfilt/(fs/2)
        self.transpose = transpose
# attain data and change it into left right and time chanel        
    def read_signal(self):
        x = str(self.path)
        x = x.split('.')[1]
        if x == "xlsx":
            raw_data = np.array(pd.read_excel(self.path))
            if self.transpose == True:
                raw_data = np.transpose(raw_data)
        else:
            raw_data = np.array(pd.read_csv(self.path))
            if self.transpose == True:
                raw_data = np.transpose(raw_data)
        self.data = []
        time = []
        for i in range(0,len(raw_data)):
            self.data.append(raw_data[i][self.chan])
            time.append(i/self.fs)
            
        return self.data, time
        
    def load_data(self):
        self.data = []
        time = []
        x = np.array(pd.read_csv(self.path))
        for i in x:
            if not (math.isnan(i[1])):
                self.data.append(i[self.chan+1])
                time.append(i[0])
        # for j in x:
        #     self.data.append(j[self.chan])


        # time = np.linspace(0,len(self.data)/self.fs,num=len(self.data))
        return self.data, time
        
#perform fast fourier transform and returns transformed dataa in x and y    
    def fast_trans(self):
        '''
        Fast Fourier Transformation (FFT) of a given wave, representing the
        amplitude of different sinusoidals (phase not considered).
        Inputs:
            xp: numpy array, as a given data.
            fs: sampling rate of xp
        Returns two Numpy arrays of frequency/amplitude from the FFT.
        '''
        n = len(self.data)
        yf = fftpack.fft(self.data)
        self.xf = np.linspace(0.0, 0.5*self.fs, n//2)
        self.Amp = (2.0/n * np.abs(yf[:n//2]))
        return self.xf, self.Amp
#notching signals
    def notch_filter(self):
        b, a = signal.iirnotch(50/125, 20)
        notched_signal = signal.filtfilt(b, a, self.data)
        self.data = notched_signal
        return(self.data)
#Butterworth bandpass filter 
    def band_pass(self):
        b, a = butter(3, [self.lowfilt, self.highfilt], btype = "bandpass")
        y = lfilter(b, a, self.data)
        self.data = y
        return self.data
#call every function    
    def call(self):
        left, right, time = self.read_signal(self.path,self.l_chan,self.r_chan)
        left_processed = self.notch_filter(left)
        right_processed = self.notch_filter(right)
        self.plot_data(left_processed, right_processed)
#plot data
    def plot_data(self, fft=True):
        if fft == True:
            data1_fftx, data1_ffty = self.fast_trans()
            # plt.figure(1)
            plt.plot(data1_fftx,((data1_ffty)))
#             plt.subplot(211)
#             plt.subplots_adjust(hspace=0.4)
            # plt.title("raw1")
            # plt.plot(self.data)
            plt.show()
#             plt.subplot(212)

#             plt.title("FFT1")
# #             plt.plot(data1_fftx[len(data1_fftx)//4:2*len(data1_fftx)//3],
# #                      data1_ffty[len(data1_fftx)//4:2*len(data1_fftx)//3])
#             plt.plot(data1_fftx[len(data1_fftx)//10:2*len(data1_fftx)//6],
#                       data1_ffty[len(data1_fftx)//10:2*len(data1_fftx)//6])
        
