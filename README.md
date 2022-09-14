Basic repository for running Stable Diffusion on AWS using Meadowrun to
automatically manage and deploy EC2 spot instances for $$$ savings.

Based on this article:
https://medium.com/@meadowrun/how-to-run-stable-diffusion-on-ec2-e447333d820

Requires an installed and configured (with keys) `awscli`

```shell
$ pip install -r requirements.txt
$ python3 meadowrun_sd.py
```