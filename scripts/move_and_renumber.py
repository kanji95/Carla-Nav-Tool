import os

NEW_PATH = "/ssd_scratch/cvit/amoghtiwari/new_data"
TRAIN_PATH = "/ssd_scratch/cvit/amoghtiwari/carla_data/train/"
batches = os.listdir(NEW_PATH)

EPISODE_COUNTER = 333
for batch in batches:
	batch_path = os.path.join(NEW_PATH, batch)
	episodes = os.listdir(batch_path)
	for episode in episodes:
		episode_path = os.path.join(batch_path, episode)
		target_path = os.path.join(TRAIN_PATH, str(EPISODE_COUNTER))
		EPISODE_COUNTER+= 1
		bash_command = "cp -r  %s %s"%(episode_path, target_path)
		print(bash_command)
		os.system(bash_command)