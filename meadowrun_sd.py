import asyncio

import meadowrun


def main():
  folder_name = "misc"
  prompt = "Violins, violets and vixens dancing under a blazing sky on Uranus, baroque"

  asyncio.run(
      meadowrun.run_command(
          'bash -c \''
          'aws s3 sync s3://tmoney-sd /var/meadowrun/machine_cache --exclude "*" '
          '--include sd-v1-4.ckpt '
          f'&& python scripts/txt2img.py --prompt "{prompt}" --plms '
          '--ckpt /var/meadowrun/machine_cache/sd-v1-4.ckpt --outdir /tmp/outputs '
          f'&& aws s3 sync /tmp/outputs s3://tmoney-sd/{folder_name}\'',
          meadowrun.AllocCloudInstance("EC2"),
          meadowrun.Resources(logical_cpu=1,
                              memory_gb=8,
                              max_eviction_rate=80,
                              gpu_memory=10,
                              flags="nvidia"),
          meadowrun.Deployment.git_repo(
              "https://github.com/hrichardlee/stable-diffusion",
              branch="meadowrun-compatibility",
              interpreter=meadowrun.CondaEnvironmentYmlFile(
                  "environment.yaml", additional_software="awscli"),
              environment_variables={
                  "TRANSFORMERS_CACHE":
                      "/var/meadowrun/machine_cache/transformers"
              })))


if __name__ == "__main__":
  main()
