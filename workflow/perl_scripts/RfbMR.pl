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
my $i=0;
my $len=scalar(@ARGV);
my $loginName=@ARGV[$i++];
my $loginPassword=@ARGV[$i++];
my $databaseName=@ARGV[$i++];
my $fn=@ARGV[$i++];
$fn =~ s/\//\\/g;#将/转换成\\，不然无法顺利删除文件
my $session = eval{
	GetSession($loginName, $loginPassword, $databaseName);
};
if (not $session) {#创建session失败
	print "== create session fail ==";
	exit;
}
#更新所有MR的状态
use Text::xSV;
my $csv = new Text::xSV;
$csv->open_file($fn);
$csv->read_header();
while ($csv->get_row()) {
    my ($mr_id, $reviewer, $introduction_phase, $impacted_unit, 
	$load_information, $resolutin_by_assignee, $problem_casued_by_assignee, 
	$files_altered_by_assignee, $test_exeCuted_by_assignee) = 
		$csv->extract(qw(mr_id reviewer introduction_phase impacted_unit 
			load_information resolutin_by_assignee problem_casued_by_assignee 
			files_altered_by_assignee test_exeCuted_by_assignee));

	#中文使用GBK编码-->OK
	my $entity = $session->GetEntity( "Dev_Defect", $mr_id);	
	$session->EditEntity($entity,"RfB");
	if ($reviewer) {
		$entity->SetFieldValue('Reviewer', $reviewer);
	}
	$entity->SetFieldValue('Introduction_Phase', $introduction_phase );
	$entity->SetFieldValue('Impacted_Unit', $impacted_unit );
	$entity->SetFieldValue('Load_Information', $load_information);
	$entity->SetFieldValue('Resolution_By', $resolutin_by_assignee);
	if ($problem_casued_by_assignee) {
		$entity->SetFieldValue('Problem_Cause_By', $problem_casued_by_assignee);
	}
	if ($files_altered_by_assignee) {
		$entity->SetFieldValue('Altered_File', $files_altered_by_assignee );
	}
	if ($test_exeCuted_by_assignee) {
		$entity->SetFieldValue('Tests_Executed_By', $test_exeCuted_by_assignee);
	}
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
CQSession::Unbuild($session);
unlink($fn);
print "== OK ==";
