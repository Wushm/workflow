use CQPerlExt;
###连接CQ###
#cqperl v.pl yubo_yang password ONS
#注意：由于通过控制台传递数据，因此不能随意使用print
=head
返回消息：
== create session fail ==
== ok ==
=cut
sub GetSession {
	my ($loginName, $loginPassword, $databaseName) = @_;
	my $databaseSet = "CQMS.UTSTARCOM.HZ";
	my $session = CQSession::Build();
	$session->UserLogon($loginName, $loginPassword, $databaseName, $databaseSet);	
	return $session;
}
sub ResolveEntity {
	my ($session, $mr_id) = @_;
	my $entity = $session->GetEntity( "Dev_Defect", $mr_id);	
	$session->EditEntity($entity,"resolve");#resolve modify
	my $Status = $entity->Validate();
	if($Status eq "") 
	{
		# 提交数据记录
		$entity->Commit();
	}
	else
	{
		# 打印错误信息
		#print $mr_id." ".$Status."\r\n";
		$entity->Revert();
	}
}
my $i=0;
my $len=scalar(@ARGV);
my $loginName=@ARGV[$i++];
my $loginPassword=@ARGV[$i++];
my $databaseName=@ARGV[$i++];
my $session = eval{
	GetSession($loginName, $loginPassword, $databaseName);
};
if (not $session) {#创建session失败
	print "== create session fail ==";
	exit;
}
#更新所有MR的状态
while($i<$len) {
	my $mr_id=@ARGV[$i++];
	$ret=eval{
		ResolveEntity($session, $mr_id);
	};
}
CQSession::Unbuild($session);
print "== ok ==";
