import numpy as np

class Airport:
    def __init__(self, end_sim):
        self.clock = 0
        self.t_next_arrival = self.gen_int_arr()
        self.t_departure0 = float('inf')
        self.t_departure1 = float('inf')
        self.t_departure2 = float('inf')
        self.t_departure3 = float('inf')
        self.num_in_q_s1 = 0
        self.num_in_q_s2 = 0
        self.num_in_q_s3 = 0
        self.state_s0 = 0
        self.state_s1 = 0
        self.state_s2 = 0
        self.state_s3 = 0
        self.end_sim = end_sim
        self.break_times = np.arange(4.0, self.end_sim + 4.0, 4.0)
        self.break_duration = 0.25
        self.total_time_q1 = 0
        self.total_time_q2 = 0
        self.total_time_q3 = 0
        self.t_q1 = 0
        self.t_q2 = 0
        self.t_q3 = 0
        self.total_passenger_s0 = 0
        self.total_passenger_s1 = 0
        self.total_passenger_s2 = 0
        self.total_passenger_s3 = 0
        self.total_off_s0 = 0
        self.total_off_s1 = 0
        self.total_off_s2 = 0
        self.total_off_s3 = 0
        self.off_s0 = 0
        self.off_s1 = 0
        self.off_s2 = 0
        self.off_s3 = 0
        
    def time_adv(self):
        t_next_event = min(self.t_next_arrival, self.t_departure0, self.t_departure1, self.t_departure2, self.t_departure3)  
        
        self.clock = t_next_event
        
        if self.clock >= self.break_times[0] + self.break_duration:
            self.break_times = np.delete(self.break_times, 0)
        
        if self.t_next_arrival == min(self.t_next_arrival, self.t_departure0, self.t_departure1, self.t_departure2, self.t_departure3):
            self.arrival()
        elif self.t_departure0 == min(self.t_next_arrival, self.t_departure0, self.t_departure1, self.t_departure2, self.t_departure3):
            self.server0()
        elif self.t_departure1 == min(self.t_next_arrival, self.t_departure0, self.t_departure1, self.t_departure2, self.t_departure3):
            self.server1()
        elif self.t_departure2 == min(self.t_next_arrival, self.t_departure0, self.t_departure1, self.t_departure2, self.t_departure3):
            self.server2()
        else:
            self.server3()
            
    def arrival(self):
        if self.num_in_q_s1 == 0:
            if self.state_s1 == 1 and self.state_s0 == 1:
                self.num_in_q_s1 += 1
                self.t_q1 = self.clock
                self.t_next_arrival = self.clock + self.gen_int_arr()
                
            elif self.state_s1 == 0:
                self.state_s1 = 1
                self.total_off_s1 += (self.clock - self.off_s1)
                self.dep1 = self.gen_service_time_s1()
                self.t_departure1 = self.clock + self.dep1
                self.t_next_arrival = self.clock + self.gen_int_arr()
                if self.t_departure1 >= self.break_times[0]:
                    self.t_departure1 += self.break_duration
                    print('break time at server1')
                    
            elif self.state_s0 == 0:
                self.state_s0 = 1
                self.total_off_s0 += (self.clock - self.off_s0)
                self.dep0 = self.gen_service_time_s1()
                self.t_departure0 = self.clock + self.dep0
                self.t_next_arrival = self.clock + self.gen_int_arr()
                if self.t_departure0 >= self.break_times[0]:
                    self.t_departure0 += self.break_duration
                    print('break time at server0')
                    
        else:
            self.num_in_q_s1 += 1
            self.t_q1 = self.clock
            self.t_next_arrival = self.clock + self.gen_int_arr()
                
    def server0(self):
        if self.num_in_q_s1 > 0:
            self.dep0 = self.gen_service_time_s1()
            self.t_departure0 = self.clock + self.dep0
            self.total_time_q1 += (self.clock - self.t_q1)*self.num_in_q_s1
            self.num_in_q_s1 -= 1
            self.total_passenger_s0 += 1
            if self.t_departure0 >= self.break_times[0]:
                self.t_departure0 += self.break_duration
                print('break time at server0')
        else:
            self.total_passenger_s0 += 1
            self.off_s0 = self.clock
            self.t_departure0 = float('inf') 
            self.state_s0 = 0
            
        if self.num_in_q_s2 == 0:
            if self.state_s2 == 1:
                self.num_in_q_s2 += 1
                self.t_q2 = self.clock
                
            elif self.state_s2 == 0:
                self.state_s2 = 1
                self.total_off_s2 += (self.clock - self.off_s2)
                self.dep2 = self.gen_service_time_s2()
                self.t_departure2 = self.clock + self.dep2
                if self.t_departure2 >= self.break_times[0]:
                    self.t_departure2 += self.break_duration
                    print('break time at server2')
        else:
            self.num_in_q_s2 += 1
            self.t_q2 = self.clock
    
    def server1(self):
        if self.num_in_q_s1 > 0:
            self.dep1 = self.gen_service_time_s1()
            self.t_departure1 = self.clock + self.dep1
            self.total_time_q1 += (self.clock - self.t_q1)*self.num_in_q_s1
            self.num_in_q_s1 -= 1
            self.total_passenger_s1 += 1
            if self.t_departure1 >= self.break_times[0]:
                self.t_departure1 += self.break_duration
                print('break time at server1')
        else:
            self.total_passenger_s1 += 1
            self.off_s1 = self.clock
            self.t_departure1 = float('inf') 
            self.state_s1 = 0
            
        if self.num_in_q_s2 == 0:
            if self.state_s2 == 1:
                self.num_in_q_s2 += 1
                self.t_q2 = self.clock
                
            elif self.state_s2 == 0:
                self.state_s2 = 1
                self.total_off_s2 += (self.clock - self.off_s2)
                self.dep2 = self.gen_service_time_s2()
                self.t_departure2 = self.clock + self.dep2
                if self.t_departure2 >= self.break_times[0]:
                    self.t_departure2 += self.break_duration
                    print('break time at server2')
        else:
            self.num_in_q_s2 += 1
            self.t_q2 = self.clock
            
            
    def server2(self):
        if self.num_in_q_s2 > 0:
            self.dep2 = self.gen_service_time_s2()
            self.t_departure2 = self.clock + self.dep2
            self.total_time_q2 += (self.clock - self.t_q2)*self.num_in_q_s2
            self.num_in_q_s2 -= 1
            self.total_passenger_s2 += 1
            if self.t_departure2 >= self.break_times[0]:
                self.t_departure2 += self.break_duration
                print('break time at server2')
        else:
            self.total_passenger_s2 += 1
            self.off_s2 = self.clock
            self.t_departure2 = float('inf') 
            self.state_s2 = 0
            
        if self.num_in_q_s3 == 0:
            if self.state_s3 == 1:
                self.num_in_q_s3 += 1
                self.t_q3 = self.clock
                
            elif self.state_s3 == 0:
                self.state_s3 = 1
                self.total_off_s3 += (self.clock - self.off_s3)
                self.dep3 = self.gen_service_time_s3()
                self.t_departure3 = self.clock + self.dep3
                if self.t_departure3 >= self.break_times[0]:
                    self.t_departure3 += self.break_duration
                    print('break time at server3')
        else:
            self.num_in_q_s3 += 1
            self.t_q3 = self.clock
            
            
    def server3(self):
        if self.num_in_q_s3 > 0:
            self.dep3 = self.gen_service_time_s3()
            self.t_departure3 = self.clock + self.dep3
            self.total_time_q3 += (self.clock - self.t_q3)*self.num_in_q_s3
            self.num_in_q_s3 -= 1
            self.total_passenger_s3 += 1
            if self.t_departure3 >= self.break_times[0]:
                self.t_departure3 += self.break_duration
                print('break time at server3')
        else:
            self.total_passenger_s3 += 1
            self.off_s3 = self.clock
            self.t_departure3 = float('inf') 
            self.state_s3 = 0
            
            
    def gen_int_arr(self):
        return np.random.exponential(scale=0.8)
    
    def gen_service_time_s1(self):
        return np.random.exponential(scale=0.7)
    
    def gen_service_time_s2(self):
        return np.random.exponential(scale=0.6)
    
    def gen_service_time_s3(self):
        return np.random.normal(loc=0.5,scale=0.1)
		
		
		
		
end_sim = 50
s = Airport(end_sim)
np.random.seed(20)
while s.clock <= end_sim :
    print("Server time:",round(s.clock,4)," Break time:",s.break_times)
    print("Off times: ",round(s.total_off_s0,4), " - ",round(s.total_off_s1,4)," - ",round(s.total_off_s2,4)," - ",round(s.total_off_s3,4))
    print("wait time in Queue: ",round(s.total_time_q1,4)," - ",round(s.total_time_q2,4)," - ",round(s.total_time_q3,4))
    print("[A,",round(s.t_next_arrival, 4), "],[C0,", round(s.t_departure0, 4), "],[C1,", round(s.t_departure1, 4), "],[C2,", round(s.t_departure2, 4),"],[C3,", round(s.t_departure3, 4))
    print(s.num_in_q_s1," - ",s.num_in_q_s2," - ",s.num_in_q_s3)
    print(s.state_s0," - ",s.state_s1," - ",s.state_s2," - ",s.state_s3)
    print(s.total_passenger_s0, " - ", s.total_passenger_s1, " - ", s.total_passenger_s2, " - ", s.total_passenger_s3)
    s.time_adv()
print("\n \nTotal number of Customers processed at Server 0: ", s.total_passenger_s0)
print("Total number of Customers processed at Server 1: ", s.total_passenger_s1)
print("Total number of Customers processed at Server 2: ", s.total_passenger_s2)
print("Total number of Customers processed at Server 3: ", s.total_passenger_s3,"\n")
print("Utilization of Server 0: ",f'{1-(s.total_off_s0/s.clock):9.4f}')
print("Utilization of Server 1: ",f'{1-(s.total_off_s1/s.clock):9.4f}')
print("Utilization of Server 2: ",f'{1-(s.total_off_s2/s.clock):9.4f}')
print("Utilization of Server 3: ",f'{1-(s.total_off_s3/s.clock):9.4f}',"\n")
print("Avarage wait time in queue1: ",f'{s.total_time_q1/(s.total_passenger_s1+s.total_passenger_s0):9.4f}')
print("Avarage wait time in queue2: ",f'{s.total_time_q2/s.total_passenger_s2:9.4f}')
print("Avarage wait time in queue3: ",f'{s.total_time_q3/s.total_passenger_s3:9.4f}',"\n")
print("Avarage service time at server 1: ",f'{((s.clock-s.total_off_s0)/s.total_passenger_s0):9.4f}')
print("Avarage service time at server 1: ",f'{((s.clock-s.total_off_s1)/s.total_passenger_s1):9.4f}')
print("Avarage service time at server 2: ",f'{((s.clock-s.total_off_s2)/s.total_passenger_s2):9.4f}')
print("Avarage service time at server 3: ",f'{((s.clock-s.total_off_s3)/s.total_passenger_s3):9.4f}')
