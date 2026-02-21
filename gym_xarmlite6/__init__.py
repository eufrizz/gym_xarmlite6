import importlib.util

if importlib.util.find_spec('gymnasium') is not None:
    from gymnasium.envs.registration import register
    register(id='UfactoryCubePickup-v0', entry_point='gym_lite6.env:UfactoryLite6Env')
