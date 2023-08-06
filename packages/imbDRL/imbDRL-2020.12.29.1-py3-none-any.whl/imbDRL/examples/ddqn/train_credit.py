import os

from imbDRL.agents.ddqn import TrainDDQN
from imbDRL.data import get_train_test_val, load_creditcard
from imbDRL.utils import rounded_dict

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # CPU is faster than GPU on structured data

episodes = 100_000  # Total number of episodes
warmup_episodes = 170_000  # Amount of warmup steps to collect data with random policy
memory_length = warmup_episodes  # Max length of the Replay Memory
batch_size = 32
collect_steps_per_episode = 2000
collect_every = 500

target_model_update = 800  # Period to overwrite the target Q-network with the default Q-network
target_update_tau = 1  # Soften the target model update
n_step_update = 1

conv_layers = None  # Convolutional layers
dense_layers = (256, 256, )  # Dense layers
dropout_layers = (0.2, 0.2, )  # Dropout layers

lr = 0.00025  # Learning rate
gamma = 0.0  # Discount factor
min_epsilon = 0.5  # Minimal and final chance of choosing random action
decay_episodes = episodes // 10  # Number of episodes to decay from 1.0 to `min_epsilon``

imb_rate = 0.001729  # Imbalance rate
min_class = [1]  # Minority classes
maj_class = [0]  # Majority classes
X_train, y_train, X_test, y_test, = load_creditcard(normalization=True)
X_train, y_train, X_test, y_test, X_val, y_val = get_train_test_val(X_train, y_train, X_test, y_test,
                                                                    min_class, maj_class, val_frac=0.2)

model = TrainDDQN(episodes, warmup_episodes, lr, gamma, min_epsilon, decay_episodes, target_model_update=target_model_update,
                  target_update_tau=target_update_tau, batch_size=batch_size, collect_steps_per_episode=collect_steps_per_episode,
                  memory_length=memory_length, collect_every=collect_every, n_step_update=n_step_update)

model.compile_model(X_train, y_train, imb_rate, conv_layers, dense_layers, dropout_layers)
model.train(X_val, y_val, "F1")

stats = model.evaluate(X_test, y_test, X_train, y_train)
print(rounded_dict(stats))
# {'Gmean': 0.886281, 'F1': 0.806283, 'Precision': 0.827957, 'Recall': 0.785714, 'TP': 77, 'TN': 56848, 'FP': 16, 'FN': 21}
