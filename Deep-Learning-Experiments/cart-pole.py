##import gym
##env = gym.make('CartPole-v0')
##env.reset()
##for _ in range(1000):
##    env.render()
##    env.step(env.action_space.sample()) # take a random action
##env.close()

from gym.envs.registration import register
import gym
from envs.foo_env import BananaEnv
from envs.foo_env import Job
from envs.foo_env import Node
from envs.foo_env import Action
import time

register(
    id='banana-v0',
    entry_point='envs:BananaEnv',
)

env = gym.make('banana-v0')
env.reset()

def fifo(env):
    if len(env.queue) == 0:
        return None
    
    # always schedule first job
    num_cores_required = env.queue[0].num_cores 
    
    for node_index in range(len(env.nodes)):
        if env.nodes[node_index].num_avail_cores >= num_cores_required:
            # schedule first job on first available node
            return Action(0,node_index)
    return None

for _ in range(10000):
    #print(len(env.queue))
    print(env)
    action = fifo(env) # scheduler returns action

    while env.take_action(action):
        # keep coming up with actions until we take an invalid action
        action = fifo(env)
        continue
    
    env.step()   # one step in time

