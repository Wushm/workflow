#########################################################################
# ���ű�ʵ��New MR�Ĺ���,��ȷ���Ƿ�֧�ֿո��Ƿ�֧�����ģ�
# input parameters:
# [����1] CQ_username:  
# [����2] CQ_password:    
# [����3] databaseName:   
# [����4] mr_info:
# Auther:    Wu Shuming
# example:   cqperl submit_new_mr.pl "smwu" "ONS" "CQMS.UTSTARCOM.HZ" "e:tmpnewmr.csv"
# History: test result:ONS00043827 
#            
#            
#########################################################################

use CQPerlExt;

### ����Ա��Ϣ###
my $adminName="wangfei";
my $adminPassword = "password";

my $i=0;

my $len=scalar(@ARGV);

###argvSubmitter �ύ������###
my $argvSubmitter = @ARGV[$i++];

###database_name ��������ONS/NMS��###
my $databaseName=@ARGV[$i++];

###database_set �⼯�����ֶζ��ں���Ϊ��"CQMS.UTSTARCOM.HZ"###
my $databaseSet = @ARGV[$i++];

###����MR������####
my $fn=@ARGV[$i++];
$fn =~ s/\//\\/g;#��/ת����\\����Ȼ�޷�˳��ɾ���ļ�

###��CQ����session��������CQ�Ŀ�###
my $session = CQSession::Build();

###��½CQ��###
$session->UserLogon($adminName, $adminPassword, $databaseName, $databaseSet);

###entitydef_name������CQ�ͻ��˴�����ѯʱ��ѡ���record type###
my $entitydef_name = "Dev_Defect";	

use Text::xSV;
my $csv = new Text::xSV;
$csv->open_file($fn);
$csv->read_header();

while ($csv->get_row()) {
	###��csv�����ȡ����#####
	my ($argvHeadline, $argvProject, $argvRelease, $argvProblem) = $csv->extract(qw(headline project found_release_number problem_description));
	#����ʹ��GBK����-->OK
	$entity = $session->BuildEntity($entitydef_name);
	$entity->SetFieldValue("Headline", $argvHeadline);
	$entity->SetFieldValue("Project", $argvProject);
	$entity->SetFieldValue("Found_Release_Number", $argvRelease);
	$entity->SetFieldValue("Problem_Description", $argvProblem);		
	$id = $entity->GetDbId();


	my $Status = $entity->Validate();
	if($Status eq "") 
	{
		# �ύ���ݼ�¼
		print $id; 
		print "\n";
		print "=== new mr success ===\n";
		$entity->Commit();
	}
	else
	{
		# ��ӡ������Ϣ
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
		# �ύ���ݼ�¼
		print "=== modify Assignee success ===\n";
		$entity->Commit();
	}
	else
	{
		# ��ӡ������Ϣ
		print "=== modify Assignee error ===\n";
		print $Status;
		$entity->Revert();
	}
	### Assign action ###
	$session->EditEntity($entity, "Assign");	
	my $Status = $entity->Validate();

	if($Status eq "") 
	{
		# �ύ���ݼ�¼
		print "=== Assign action success ===\n";
		$entity->Commit();
	}
	else
	{
		# ��ӡ������Ϣ
		print "=== Assign action error ===\n";
		print $Status;
		ntity->Revert();
	}
}

CQSession::Unbuild($session);

unlink $fn;

exit(0);
