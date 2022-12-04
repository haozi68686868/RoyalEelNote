```
aws --endpoint-url=http://10.5.41.234:80  s3 ls s3://sh40_fieldtest_master/2020_08/
```

CI账号

```
dev_role
senseauto@dev
```

commit and push

```
git push origin HEAD:refs/for/develop%topic=TEDS-135_launcher_adapt_for_BYNAV_device
```

下载deb包

```
sudo apt update && apt download ****** # ******的deb编号可以从CI找到
# 下载master包

# 下载历史包
http://k8s.senseauto.com:30020/root/packages/
```

devcenter密码

```
a5f13467024efa2c
```

