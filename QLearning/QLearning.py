import numpy as np

class Env:
    def __init__(self, states):
        self.normal = states[0]
        self.tumor = states[1]
        self.immune = states[2]
        self.drug_con = states[3]
    
    def _update(self, u):
        parameters_a = [0.2,0.3,0.1]
        parameters_b = [1,1]
        parameters_c = [1,0.5,1,1]
        parameters_d = [0.2,1]
        parameters_r = [1.5,1]
        s = 0.33
        alpha = 0.3
        rho = 0.01
        return Env([
            self.normal+(parameters_r[1]*self.normal*(1-parameters_b[1]*self.normal)-parameters_c[3]*self.normal*self.tumor-parameters_a[2]*self.normal*self.drug_con)*0.1,
            self.tumor+(parameters_r[0]*self.tumor*(1-parameters_b[0]*self.tumor)-parameters_c[1]*self.immune*self.tumor-parameters_c[2]*self.tumor*self.normal-parameters_a[1]*self.tumor*self.drug_con)*0.1,
            self.immune+(s+(rho*self.immune*self.tumor)/(alpha+self.tumor)-parameters_c[0]*self.immune*self.tumor-parameters_d[0]*self.immune-parameters_a[0]*self.immune*self.drug_con)*0.1,
            self.drug_con+(-parameters_d[1]*self.drug_con+u)*0.1
        ])


u_max=10
action_space = np.linspace(0,u_max,num=50)
state_space = np.arange(0,20,1)


epoch = []

def reward(e_1,e_2):
    if e_2<e_1:
        return (e_1-e_2)/e_1
    return 0

state_table=[0.0063,0.0125,0.025,0.01,0.05,0.1,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.8,0.9,np.inf]

def state_update(error):
    ix = 0
    while error>state_table[ix]:
        ix+=1
    return ix

q_table=np.zeros([len(state_space), len(action_space)])

for i in range(10000):
    env = Env([0.6,1,0.9,0.5])
    state = [state_update(env.tumor)]
    error = [env.tumor]
    actions = []

    a=0.1
    g=0.6
    epsilon=0.1
    done = False
    while not done:
        p = np.random.random()
        if p<epsilon:
            ix = np.random.randint(0,len(action_space))
            action = action_space[ix]
        else:
            ix = np.argmax(q_table[state])
            action = action_space[ix]
        env = env._update(action)
        next_state = state_update(env.tumor)
        r = reward(error[-1],env.tumor)
        if state==0:
            done=True
        old_value = q_table[state,ix]
        next_max = np.max(q_table[next_state])

        new_value = old_value+g*(r+g*next_max-old_value) 
        q_table[state,ix]=new_value
        state = next_state
print(q_table)


