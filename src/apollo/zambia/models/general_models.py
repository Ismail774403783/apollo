from django.db import models
from webapp.models import ChecklistResponse, IncidentResponse, Checklist, Incident
from django.core.validators import RegexValidator
from django.db.models.signals import post_save

# Create your models here.
class ZambiaChecklistResponse(ChecklistResponse):
    OPTIONS_A = (
        (1, 'Before 6am'),
        (2, 'At 6am'),
        (3, 'Between 6am and 7am'),
        (4, 'After 9am')
    )
    YES_NO = (
        (1, 'Yes'),
        (2, 'No')
    )
    YES_NO_NONE = (
        (1, 'Yes'),
        (2, 'No'),
        (3, 'No One in Queue')
    )
    OPTIONS_CB = (
        (1, '3 boxes present'),
        (2, '2 boxes present'),
        (3, '1 box present')
    )
    OPTIONS_CC = (
        (1, 'correct ballots'),
        (2, 'no ballots'),
    )
    OPTIONS_CD = (
        (1, 'correct ballots'),
        (2, 'wrong ballots'),
        (3, 'no ballots')
    )
    OPTIONS_K = (
        (1, 'None(0)'),
        (2, 'Few(1-5)'),
        (3, 'Some(6-25)'),
        (4, 'Many(26+)')
    )
    # identification
    monitor_name = models.CharField(blank=True, max_length=100)
    monitor_phone = models.CharField(blank=True, max_length=100)
    
    # setup
    A = models.IntegerField(blank=True, null=True, choices=OPTIONS_A, validators=[RegexValidator(r'[1-4]')], help_text='At what time did people start voting at your polling stream? (if voting has not commenced by 9am complete a critical incident form)')
    B = models.IntegerField(blank=True, null=True, choices=YES_NO, validators=[RegexValidator(r'[1-2]')], help_text='Was the polling stream set up so that voters could mark their ballot in secret? (if "No" complete a critical incident form)')
    CA = models.IntegerField(blank=True, null=True, choices=YES_NO, validators=[RegexValidator(r'[1-2]')], help_text='Did the polling stream have Indelible Markers')
    CB = models.IntegerField(blank=True, null=True, choices=OPTIONS_CB, validators=[RegexValidator(r'[1-3]')], help_text='Did the polling stream have Three Ballot Boxes (Presidential, Parliamentary/National Assembly and Local Government)')
    CC = models.IntegerField(blank=True, null=True, choices=OPTIONS_CC, validators=[RegexValidator(r'[1-2]')], help_text='Presidential Ballot Papers - Orange')
    CD = models.IntegerField(blank=True, null=True, choices=OPTIONS_CC, validators=[RegexValidator(r'[1-3]')], help_text='Parliamentary/National Assembly Ballot Papers - Red ')
    CE = models.IntegerField(blank=True, null=True, choices=OPTIONS_CC, validators=[RegexValidator(r'[1-3]')], help_text='Local Government Ballot Papers - Black and White')
    CF = models.IntegerField(blank=True, null=True, choices=YES_NO, validators=[RegexValidator(r'[1-2]')], help_text='Official Stamp/Mark')
    CG = models.IntegerField(blank=True, null=True, choices=YES_NO, validators=[RegexValidator(r'[1-2]')], help_text='Final Voters\' Register')
    CH = models.IntegerField(blank=True, null=True, choices=YES_NO, validators=[RegexValidator(r'[1-2]')], help_text='Polling Booths')
    D = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'\d+')], help_text='How many polling officials were present at the polling stream?')
    E = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'\d+')], help_text='How many political party polling agents were present at the polling stream?')
    EA = models.IntegerField(blank=True, null=True, choices=YES_NO, validators=[RegexValidator(r'[1-3]')], help_text='Was a polling agent present for MMD?')
    EB = models.IntegerField(blank=True, null=True, choices=YES_NO, validators=[RegexValidator(r'[1-2]')], help_text='Was a polling agent present for Patriotic Front?')
    EC = models.IntegerField(blank=True, null=True, choices=YES_NO, validators=[RegexValidator(r'[1-2]')], help_text='Was a polling agent present for UPND?')
    F = models.IntegerField(blank=True, null=True, choices=YES_NO, validators=[RegexValidator(r'[1-2]')], help_text='Were uniformed police present at the polling stream?')
    G = models.IntegerField(blank=True, null=True, choices=YES_NO, validators=[RegexValidator(r'[1-2]')], help_text='Were all ballot boxes present shown to be empty before they were closed and sealed?(if "No" complete a critical incident form)')
    H = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'\d+')], help_text='How many people are registered at the polling stream?')
    J = models.CharField(blank=True, null=True, max_length=100, validators=[RegexValidator(r'\d+')], help_text='What is the ECZ\'s six digit ID number of the polling station of your polling stream')
    
    # voting
    K = models.IntegerField(blank=True, null=True, choices=OPTIONS_K, validators=[RegexValidator(r'[1-4]')], help_text='How many people with a NRC and voter\'s card were not permitted to vote because their name did not appear on the voter\'s register')
    M = models.IntegerField(blank=True, null=True, choices=OPTIONS_K, validators=[RegexValidator(r'[1-4]')], help_text='How many people were permitted to vote even though they did not have their NRC and voter\'s card?')    
    N = models.IntegerField(blank=True, null=True, choices=OPTIONS_K, validators=[RegexValidator(r'[1-4]')], help_text='How many people were permitted to vote even though their name was not in the voter\'s register?')
    P = models.IntegerField(blank=True, null=True, choices=OPTIONS_K, validators=[RegexValidator(r'[1-4]')], help_text='How many people who requested assistance in voting were denied assistance?')    
    Q = models.IntegerField(blank=True, null=True, choices=OPTIONS_K, validators=[RegexValidator(r'[1-4]')], help_text='How many people were permitted to vote on behalf of someone other than themselves?')
    R = models.IntegerField(blank=True, null=True, choices=OPTIONS_K, validators=[RegexValidator(r'[1-4]')], help_text='How many people who voted were not marked with indelible ink?')    
    S = models.IntegerField(blank=True, null=True, choices=YES_NO, validators=[RegexValidator(r'[1-2]')], help_text='At any time, did any campaigning occur inside or near the polling stream?')
    T = models.IntegerField(blank=True, null=True, choices=YES_NO, validators=[RegexValidator(r'[1-2]')], help_text='At any time, were uniformed security personnel present in the polling stream without permission of the election officials?')
    U = models.IntegerField(blank=True, null=True, choices=YES_NO, validators=[RegexValidator(r'[1-2]')], help_text='At any time, were unauthorised persons permitted in the polling stream?')
    V = models.IntegerField(blank=True, null=True, choices=YES_NO, validators=[RegexValidator(r'[1-2]')], help_text='Were there any incidents of intimidation or violence at the polling stream? (if "Yes" complete a critical incident form)')
    W = models.IntegerField(blank=True, null=True, choices=YES_NO, validators=[RegexValidator(r'[1-2]')], help_text='At any time, was the voting process suspended for more than 30 minutes? (if "Yes" complete a critical incident form)')
    
    # closing
    X = models.IntegerField(blank=True, null=True, choices=OPTIONS_K, validators=[RegexValidator(r'[1-4]')], help_text='How many people were in still in the queue waiting to vote at 18h00?')    
    Y = models.IntegerField(blank=True, null=True, choices=YES_NO_NONE, validators=[RegexValidator(r'[1-3]')], help_text='Was everyone in the queue waiting to vote at 18h00 permitted to vote')
    Z = models.IntegerField(blank=True, null=True, choices=YES_NO, validators=[RegexValidator(r'[1-2]')], help_text='Was anyone permitted to join the queue and vote after 18h00?')
    AA = models.IntegerField(blank=True, null=True, choices=YES_NO, validators=[RegexValidator(r'[1-2]')], help_text='Were the opening slots of all ballot boxes sealed closed after everyone had voted?')
    
    # counting
    AB   = models.IntegerField(blank=True, null=True, choices=YES_NO, validators=[RegexValidator(r'[1-2]')], help_text='Were all polling agents permitted to observe the counting of ballot papers? (if "No" complete a critical incident form)')
    AC   = models.IntegerField(blank=True, null=True, choices=YES_NO, validators=[RegexValidator(r'[1-2]')], help_text='Were any unauthorized persons present during counting? (if "Yes" complete a critical incident form)')
    AD   = models.IntegerField(blank=True, null=True, choices=YES_NO, validators=[RegexValidator(r'[1-2]')], help_text='Were there any incidents of intimidation during counting? (if "Yes" complete a critical incident form)')
    AEAA = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Ballot Papers Received at Your Assigned Stream(Presidential)')
    AEAB = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Ballot Papers Received at Entire Polling Station(Presidential )')
    AEAC = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Ballot Papers Received at Your Assigned Stream(Parliamentary )')
    AEAD = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Ballot Papers Received at Entire Polling Station(Parliamentary )')
    AEAE = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Ballot Papers Received at Your Assigned Stream(Local Government )')
    AEAF = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Ballot Papers Received at Entire Polling Station(Local Government )')
    AEBA = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Unused Ballot Papers at Your Assigned Stream(Presidential )')
    AEBB = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Unused Ballot Papers at Entire Polling Station(Presidential )')
    AEBC = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Unused Ballot Papers at Your Assigned Stream(Parliamentary )')
    AEBD = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Unused Ballot Papers at Entire Polling Statio(Parliamentary n)')
    AEBE = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Unused Ballot Papers at Your Assigned Stream(Local Government )')
    AEBF = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Unused Ballot Papers at Entire Polling Station(Local Government )')
    AECA = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Issued Ballot Papers at Your Assigned Stream(Presidential )')
    AECB = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Issued Ballot Papers at Entire Polling Station(Presidential )')
    AECC = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Issued Ballot Papers at Your Assigned Stream(Parliamentary )')
    AECD = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Issued Ballot Papers at Entire Polling Station(Parliamentary )')
    AECE = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Issued Ballot Papers at Your Assigned Stream(Local Government )')
    AECF = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Issued Ballot Papers at Entire Polling Station(Local Government )')
    AEDA = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Spoilt Ballot Papers at Your Assigned Stream(Presidential )')
    AEDB = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Spoilt Ballot Papers at Entire Polling Station(Presidential )')
    AEDC = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Spoilt Ballot Papers at Your Assigned Stream(Parliamentary )')
    AEDD = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Spoilt Ballot Papers at Entire Polling Station(Parliamentary )')
    AEDE = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Spoilt Ballot Papers at Your Assigned Stream(Local Government )')
    AEDF = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Spoilt Ballot Papers at Entire Polling Station(Local Government )')
    AEEA = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Ballot Papers Found in the Ballot Box at Your Assigned Stream(Presidential )')
    AEEB = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Ballot Papers Found in the Ballot Box at Entire Polling Station(Presidential )')
    AEEC = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Ballot Papers Found in the Ballot Box at Your Assigned Stream(Parliamentary )')
    AEED = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Ballot Papers Found in the Ballot Box at Entire Polling Station(Parliamentary )')
    AEEE = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Ballot Papers Found in the Ballot Box at Your Assigned Stream(Local Government )')
    AEEF = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Ballot Papers Found in the Ballot Box at Entire Polling Station(Local Government)')
    AFAA = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Rejected Ballot Papers at Your Assigned Stream(Presidential )')
    AFAB = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Rejected Ballot Papers at Entire Polling Station(Presidential )')
    AFAC = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Rejected Ballot Papers at Your Assigned Stream(Parliamentary )')
    AFAD = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Rejected Ballot Papers at Entire Polling Station(Parliamentary )')
    AFAE = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Rejected Ballot Papers at Your Assigned Stream(Local Government )')
    AFAF = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Rejected Ballot Papers at Entire Polling Station(Local Government)')
    AFBA = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Presidential )')
    AFBB = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Presidential )')
    AFBC = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Parliamentary )')
    AFBD = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Parliamentary )')
    AFBE = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Local Government )')
    AFBF = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Local Government)')
    AFCA = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Presidential )')
    AFCB = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Presidential )')
    AFCC = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Parliamentary )')
    AFCD = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Parliamentary )')
    AFCE = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Local Government )')
    AFCF = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Local Government)')
    AFDA = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Presidential )')
    AFDB = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Presidential )')
    AFDC = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Parliamentary )')
    AFDD = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Parliamentary )')
    AFDE = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Local Government )')
    AFDF = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Local Government)')
    AFEA = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Presidential )')
    AFEB = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Presidential )')
    AFEC = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Parliamentary )')
    AFED = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Parliamentary )')
    AFEE = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Local Government )')
    AFEF = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Local Government)')
    AFFA = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Presidential )')
    AFFB = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Presidential )')
    AFFC = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Parliamentary )')
    AFFD = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Parliamentary )')
    AFFE = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Local Government )')
    AFFF = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Local Government)')
    AFGA = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Presidential )')
    AFGB = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Presidential )')
    AFGC = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Parliamentary )')
    AFGD = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Parliamentary )')
    AFGE = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Local Government )')
    AFGF = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Local Government)')
    AFHA = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Presidential )')
    AFHB = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Presidential )')
    AFHC = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Parliamentary )')
    AFHD = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Parliamentary )')
    AFHE = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Local Government )')
    AFHF = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Local Government)')
    AFJA = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Presidential )')
    AFJB = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Presidential )')
    AFJC = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Parliamentary )')
    AFJD = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Parliamentary )')
    AFJE = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Local Government )')
    AFJF = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Local Government)')
    AFKA = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Presidential )')
    AFKB = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Presidential )')
    AFKC = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Parliamentary )')
    AFKD = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Parliamentary )')
    AFKE = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Local Government )')
    AFKF = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Local Government)')
    AFMA = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Presidential )')
    AFMB = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Presidential )')
    AFMC = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Parliamentary )')
    AFMD = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Parliamentary )')
    AFME = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Local Government )')
    AFMF = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Local Government)')
    AFNA = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Presidential )')
    AFNB = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Presidential )')
    AFNC = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Parliamentary )')
    AFND = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Parliamentary )')
    AFNE = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Local Government )')
    AFNF = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Local Government)')
    AFPA = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Presidential )')
    AFPB = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Presidential )')
    AFPC = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Parliamentary )')
    AFPD = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Parliamentary )')
    AFPE = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Local Government )')
    AFPF = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Local Government)')
    AFQA = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Presidential )')
    AFQB = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Presidential )')
    AFQC = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Parliamentary )')
    AFQD = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Parliamentary )')
    AFQE = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Your Assigned Stream(Local Government )')
    AFQF = models.IntegerField(blank=True, null=True, validators=[RegexValidator(r'[\d+]')], help_text='Number of Disputed Ballots at Entire Polling Station(Local Government)')
    AG   = models.IntegerField(blank=True, null=True, choices=YES_NO, validators=[RegexValidator(r'[1-2]')], help_text='Did you agree with the presidential results for your polling stream?')
    AH   = models.IntegerField(blank=True, null=True, choices=YES_NO, validators=[RegexValidator(r'[1-2]')], help_text='Did all polling agents present agree with the presidentialresults for your polling stream?')
    AJ   = models.IntegerField(blank=True, null=True, choices=YES_NO, validators=[RegexValidator(r'[1-2]')], help_text='Were all polling agents present given a copy of the official results for the polling station?')
    AK   = models.IntegerField(blank=True, null=True, choices=YES_NO, validators=[RegexValidator(r'[1-2]')], help_text='Were the official results for the polling station posted for the public to see?')
    created = models.DateTimeField(blank=False, auto_now_add=True)
    updated = models.DateTimeField(blank=False, auto_now=True)
    
    class Admin:
        list_display = ('',)
        search_fields = ('',)
    
    class Meta:
        app_label = 'zambia'

    def __unicode__(self):
        return str(self.checklist.id)

class ZambiaIncidentResponse(IncidentResponse):
    OPTIONS_W = (
        (1, 'I witnessed the incident'),
        (2, 'I arrived just after the incident happened'),
        (3, 'The incident was reported to me by someone else')
    )
    monitor_name = models.CharField(blank=True, max_length=100)
    monitor_phone = models.CharField(blank=True, max_length=100)
    
    W = models.IntegerField(blank=True, null=True, choices=OPTIONS_W, validators=[RegexValidator(r'[1-3]')], help_text='Witness')
    
    A = models.NullBooleanField(blank=False, help_text='Polling stream did not open')
    B = models.NullBooleanField(blank=False, help_text='Polling stream opened very late')
    C = models.NullBooleanField(blank=False, help_text='Polling stream closed very early')
    D = models.NullBooleanField(blank=False, help_text='Polling stream did not have materials at opening')
    E = models.NullBooleanField(blank=False, help_text='Voting buying/bribery')
    F = models.NullBooleanField(blank=False, help_text='Monitor denied access to polling stream')
    G = models.NullBooleanField(blank=False, help_text='Monitor not permitted to use reporting form')
    H = models.NullBooleanField(blank=False, help_text='Police officers inside polling station')
    I = models.NullBooleanField(blank=False, help_text='Polling stream ran out of materials')
    J = models.NullBooleanField(blank=False, help_text='People in the queue at the time of official close of the polling station not allowed to vote')
    K = models.NullBooleanField(blank=False, help_text='Violence/intimidation in or near the polling station')
    K1 = models.NullBooleanField(blank=False, help_text='Uniformed police')
    K2 = models.NullBooleanField(blank=False, help_text='Party supporters')
    K4 = models.NullBooleanField(blank=False, help_text='Others')
    L = models.NullBooleanField(blank=False, help_text='Violation of voting or counting procedures')
    M = models.NullBooleanField(blank=False, help_text='Stealing or damaging of ballots')
    N = models.NullBooleanField(blank=False, help_text='Voting or counting suspended during the process for more than 30 minutes')
    O = models.TextField(blank=False, help_text='Others')
    description = models.TextField(blank=True, help_text='Description of incident')
    created = models.DateTimeField(blank=False, auto_now_add=True)
    updated = models.DateTimeField(blank=False, auto_now=True)

    class Admin:
        list_display = ('',)
        search_fields = ('',)
    
    class Meta:
        app_label = 'zambia'

    def __unicode__(self):
        return str(self.incident.id)

def checklist_callback(sender, **kwargs):
    if not hasattr(kwargs['instance'], 'response'):
        response = ZambiaChecklistResponse.objects.create(checklist=kwargs['instance'])

def incident_callback(sender, **kwargs):
    if not hasattr(kwargs['instance'], 'response'):
        response = ZambiaIncidentResponse.objects.create(incident=kwargs['instance'])

post_save.connect(checklist_callback, sender=Checklist)
post_save.connect(incident_callback, sender=Incident)