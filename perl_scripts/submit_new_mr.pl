#########################################################################
# 本脚本实现New MR的功能,不确定是否支持空格，是否支持中文？
# input parameters:
# [参数1] CQ_username:  
# [参数2] CQ_password:    
# [参数3] databaseName:   
# [参数4] mr_info:
# Auther:    Wu Shuming
# example:   cqperl submit_new_mr.pl "smwu" "ONS" "CQMS.UTSTARCOM.HZ" "e:tmpnewmr.csv"
# History: test result:ONS00043827 
#            
#            
#########################################################################

use CQPerlExt;

### 管理员信息###
my $adminName="wangfei";
my $adminPassword = "password";

my $i=0;

my $len=scalar(@ARGV);

###argvSubmitter 提交者名字###
my $argvSubmitter = @ARGV[$i++];

###database_name 库名，如ONS/NMS等###
my $databaseName=@ARGV[$i++];

###database_set 库集。该字段对于杭州为："CQMS.UTSTARCOM.HZ"###
my $databaseSet = @ARGV[$i++];

###关于MR的描述####
my $fn=@ARGV[$i++];
$fn =~ s/\//\\/g;#将/转换成\\，不然无法顺利删除文件

###和CQ建立session，连接上CQ的库###
my $session = CQSession::Build();

###登陆CQ库###
$session->UserLogon($adminName, $adminPassword, $databaseName, $databaseSet);

###entitydef_name就是在CQ客户端创建查询时候选择的record type###
my $entitydef_name = "Dev_Defect";	

use Text::xSV;
my $csv = new Text::xSV;
$csv->open_file($fn);
$csv->read_header();

while ($csv->get_row()) {
	###从csv里面获取数据#####
	my ($argvHeadline, $argvProject, $argvRelease, $argvProblem) = $csv->extract(qw(headline project found_release_number problem_description));
	#中文使用GBK编码-->OK
	$entity = $session->BuildEntity($entitydef_name);
	$entity->SetFieldValue("Headline", $argvHeadline);
	$entity->SetFieldValue("Project", $argvProject);
	$entity->SetFieldValue("Found_Release_Number", $argvRelease);
	$entity->SetFieldValue("Problem_Description", $argvProblem);		
	$id = $entity->GetDbId();


	my $Status = $entity->Validate();
	if($Status eq "") 
	{
		# 提交数据记录
		print $id; 
		print "\n";
		print "=== new mr success ===\n";
		$entity->Commit();
	}
	else
	{
		# 打印错误信息
		print $id; 
		print "\n";
		print "=== new mr error ===\n";
		$entity->Revert();
	}	
	
	$entity = $session->GetEntityByDbId($entitydef_name, $id);	

	### modify action ###
	$session->EditEntity($entity, "Modify");
	$entity->SetFieldValue("Assignee", $argvSubmitter);
	$entity->SetFieldValue("ddts_id", "sw_selftest");
	$entity->SetFieldValue("Note_Entry", "mr submitted by software team self");				

	my $Status = $entity->Validate();	
	if($Status eq "") 
	{
		# 提交数据记录
		print "=== modify Assignee success ===\n";
		$entity->Commit();
	}
	else
	{
		# 打印错误信息
		print "=== modify Assignee error ===\n";
		print $Status;
		$entity->Revert();
	}
	### Assign action ###
	$session->EditEntity($entity, "Assign");	
	my $Status = $entity->Validate();

	if($Status eq "") 
	{
		# 提交数据记录
		print "=== Assign action success ===\n";
		$entity->Commit();
	}
	else
	{
		# 打印错误信息
		print "=== Assign action error ===\n";
		print $Status;
		ntity->Revert();
	}
}

CQSession::Unbuild($session);

unlink $fn;

exit(0);
