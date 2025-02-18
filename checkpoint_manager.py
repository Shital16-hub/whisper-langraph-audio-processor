import json
import os

class CheckpointManager:
    def __init__(self, checkpoint_file):
        self.checkpoint_file = checkpoint_file
        self.checkpoint = self.load_checkpoint()

    def load_checkpoint(self):
        """Load checkpoint if it exists, else return an empty dictionary."""
        if os.path.exists(self.checkpoint_file):
            with open(self.checkpoint_file, 'r') as file:
                return json.load(file)
        return {}

    def save_checkpoint(self):
        """Save the current checkpoint to the file."""
        with open(self.checkpoint_file, 'w') as file:
            json.dump(self.checkpoint, file)

    def update_checkpoint(self, file_name, step):
        """Update the checkpoint with the file and current processing step."""
        if file_name not in self.checkpoint:
            self.checkpoint[file_name] = []
        if step not in self.checkpoint[file_name]:
            self.checkpoint[file_name].append(step)
        self.save_checkpoint()

    def get_checkpoint(self, file_name):
        """Get the list of completed steps for a file."""
        return self.checkpoint.get(file_name, [])
