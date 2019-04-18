import pwd
import grp
from resource_management import *


class KylinQuery(Script):
    def install(self, env):
        import params
        env.set_params(params)

        # Create user and group for kylin if they don't exist
        try:
            grp.getgrnam(params.kylin_group)
        except KeyError:
            Group(group_name=params.kylin_group)

        try:
            pwd.getpwnam(params.kylin_user)
        except KeyError:
            User(username=params.kylin_user,
                 gid=params.kylin_group,
                 groups=[params.kylin_group],
                 ignore_failures=True
                 )
        # create kylin directories
        Directory([params.kylin_install_dir, params.kylin_log_dir, params.kylin_pid_dir],
                  mode=0755,
                  cd_access='a',
                  create_parents=True
                  )
        # download kylin-2.5.1.tar.gz
        Execute('wget {0} -O kylin-2.5.1.tar.gz'.format(params.kylin_download))
        # Install kylin
        Execute('tar -zxvf kylin-2.5.1.tar.gz -C {0}'.format(params.kylin_install_dir))
        # Remove kylin installation file
        Execute('rm -rf kylin-2.5.1.tar.gz')
        # Ensure all files owned by kylin user:group
        cmd = format("chown -R {kylin_user}:{kylin_group} {kylin_install_dir}")
        Execute(cmd)
        # create hadoop_conf_dir
        File(format("{tmp_dir}/kylin_init.sh"),
             content=Template("init.sh.j2"),
             owner=params.kylin_user,
             group=params.kylin_group,
             mode=0o700
             )
        File(format("{tmp_dir}/kylin_env.rc"),
             content=Template("env.rc.j2"),
             owner=params.kylin_user,
             group=params.kylin_group,
             mode=0o700
             )

    def configure(self, env):
        import params
        env.set_params(params)
        kylin_properties = InlineTemplate(params.kylin_properties)
        File(format("{kylin_install_dir}/conf/kylin.properties"),
             owner=params.kylin_user,
             group=params.kylin_group,
             content=kylin_properties)
        Execute(format("chown -R {kylin_user}:{kylin_group} {kylin_log_dir} {kylin_pid_dir}"))
        cmd = format("sh {tmp_dir}/kylin_init.sh")
        Execute(cmd, user=params.kylin_user)
        cmd = format("sh {kylin_install_dir}/bin/check-env.sh")
        Execute(cmd, user="hdfs")
        # chown kylin:hdfs to /kylin
        Execute("hadoop fs -chown -R kylin:hdfs /kylin", user="hdfs")

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        cmd = format(
            ". {tmp_dir}/kylin_env.rc;{kylin_install_dir}/bin/kylin.sh start;sleep 5s;cp -rf {kylin_install_dir}/pid {kylin_pid_file}")
        Execute(cmd, user=params.kylin_user)

    def stop(self, env):
        import params
        env.set_params(params)
        cmd = format("{kylin_install_dir}/bin/kylin.sh stop")
        File(params.kylin_pid_file,
             action="delete",
             owner=params.kylin_user
             )
        Execute(cmd, user=params.kylin_user)

    def restart(self, env):
        self.stop(env)
        self.start(env)

    def status(self, env):
        check_process_status('/var/run/kylin/kylin.pid')


if __name__ == "__main__":
    KylinQuery().execute()
