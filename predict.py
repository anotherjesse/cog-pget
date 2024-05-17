from cog import BasePredictor, Input, Path
import subprocess
import time
import os
import shutil


class Predictor(BasePredictor):
    def setup(self) -> None:
        """Load the model into memory to make running multiple predictions efficient"""
        # self.model = torch.load("./weights.pth")

    def predict(
        self,
        url: str = Input(description="URL to download"),
        extract: bool = Input(default=False, description="Extract the tar file"),
        chunk_size: str = Input(default="125M", description="Chunk size (in bytes) to use when downloading a file (e.g. 10M)"),
        concurrency: int = Input(default=32, description="Maximum number of concurrent downloads/maximum number of chunks for a given file")
    ) -> Path:
        """Run a single prediction on the model"""

        start = time.time()

        print("checking pget")
        subprocess.check_call(["pget", "--help"], close_fds=True)

        if os.path.exists("tmp"):
            subprocess.check_call(["rm", "-rf", "tmp"], close_fds=True)

        print("downloading")
        cmd = ["pget"]
        if extract:
            cmd.append("--extract")
        if chunk_size:
            cmd.append("--chunk-size")
            cmd.append(chunk_size)
        if concurrency:
            cmd.append("--concurrency")
            cmd.append(str(concurrency))
        cmd.append(url)
        cmd.append("tmp")
        print(cmd)
        print("prep time: ", time.time() - start)

        start = time.time()
        subprocess.check_call(cmd, close_fds=True)
        print("download time: ", time.time() - start)

        subprocess.check_call(["find", "tmp", "-type", "f", "-exec", "ls", "-lh", "{}", ";"], close_fds=True)
