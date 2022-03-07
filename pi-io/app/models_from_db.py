# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Enum, Float, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import INTEGER, LONGTEXT, TEXT, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class 108Alert(Base):
    __tablename__ = '108_alert'

    id = Column(INTEGER(11), primary_key=True)
    userID = Column(INTEGER(11))
    sboxSerialKey = Column(String(20))
    monitor = Column(Enum('sBoxtag', 'sBoxstatus'))
    tag = Column(String(30))
    vMin = Column(Float)
    vMax = Column(Float)
    status_condition = Column(String(10))
    vFreq = Column(INTEGER(11))
    vFreq_Man = Column(INTEGER(11), server_default=text("0"))
    vNum = Column(INTEGER(11), server_default=text("0"))
    alertNum = Column(INTEGER(11))
    alertNum_Man = Column(INTEGER(11))
    countAlertNum = Column(INTEGER(11), server_default=text("0"))
    countAlertNum_Man = Column(INTEGER(11), server_default=text("0"))
    alertDay = Column(String(50))
    alertStatus = Column(Enum('active', ''), server_default=text("''"))
    createDatetime = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    valueTxt = Column(String(20))
    txt = Column(Text)


class 108AlertHistory(Base):
    __tablename__ = '108_alert_history'

    id = Column(INTEGER(11), primary_key=True)
    serialKey = Column(String(20))
    vipMsg = Column(Enum('Y', 'N'), server_default=text("'N'"))
    msg = Column(Text)
    tagType = Column(Enum('sBoxstatus', 'sBoxtag'))
    tag = Column(String(30))
    valueAlert = Column(String(50))
    createDatetime = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))


class 108AlertMsg(Base):
    __tablename__ = '108_alert_msg'

    id = Column(INTEGER(11), primary_key=True)
    sBoxSerialKey = Column(String(20))
    alertID = Column(INTEGER(11))
    linetokenID = Column(INTEGER(11), server_default=text("0"))
    linetokenID_Man = Column(INTEGER(11), server_default=text("0"))
    msg = Column(String(256))
    msg_Man = Column(String(256))
    msgShort = Column(String(30))
    msgShort_Man = Column(String(30))
    userID = Column(INTEGER(11))
    createDatetime = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))


class 108App(Base):
    __tablename__ = '108_app'

    id = Column(INTEGER(11), primary_key=True)
    sboxID = Column(INTEGER(11), nullable=False, index=True)
    userID = Column(INTEGER(11), nullable=False, index=True)
    appID = Column(String(100), nullable=False)


class 108Asset(Base):
    __tablename__ = '108_asset'

    id = Column(INTEGER(11), primary_key=True)
    assetName = Column(String(100))
    img = Column(String(100))
    userID = Column(INTEGER(11), nullable=False)
    assetCreateDate = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"))


class 108Customer(Base):
    __tablename__ = '108_customers'

    id = Column(INTEGER(11), primary_key=True)
    tokenID = Column(String(255), nullable=False)
    userMember = Column(LONGTEXT, nullable=False)
    companyName = Column(String(100), nullable=False)
    address = Column(String(100), nullable=False)
    createDate = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"))


class 108CustomersProfile(Base):
    __tablename__ = '108_customers_profile'

    id = Column(INTEGER(11), primary_key=True)
    userID = Column(INTEGER(11))
    siteName = Column(String(100))
    imgLogo = Column(String(250))
    imgLogin = Column(String(250))


class 108FactoryType(Base):
    __tablename__ = '108_factory_type'

    id = Column(INTEGER(11), primary_key=True)
    factoryType = Column(String(20), nullable=False)


class 108JobsCustomer(Base):
    __tablename__ = '108_jobs_customer'

    id = Column(INTEGER(11), primary_key=True)
    customer = Column(String(50))
    poNumber = Column(String(20))
    descPO = Column(String(255))
    process = Column(INTEGER(11), server_default=text("0"))
    qty = Column(INTEGER(11))
    duedate = Column(Date)
    userID = Column(INTEGER(11))
    dateCreate = Column(TIMESTAMP, server_default=text("current_timestamp()"))
    deleteStatus = Column(Enum('Y', 'N'), server_default=text("'N'"))
    statusDone = Column(Enum('Y', 'N'), server_default=text("'N'"))


class 108JobsCustomerDetail(Base):
    __tablename__ = '108_jobs_customer_detail'

    id = Column(INTEGER(11), primary_key=True)
    jobCustomerID = Column(INTEGER(11))
    partNo = Column(String(20))
    descPO = Column(String(255))
    matt = Column(Enum('Y', 'N'), server_default=text("'N'"))
    qty = Column(INTEGER(11))
    store = Column(INTEGER(11), server_default=text("0"))
    delivery = Column(INTEGER(11), server_default=text("0"))
    statusItem = Column(String(50))
    approve = Column(Enum('Y', 'N'), server_default=text("'N'"))
    deleteStatus = Column(Enum('Y', 'N'), server_default=text("'N'"))
    dateCreate = Column(TIMESTAMP, server_default=text("current_timestamp()"))


class 108JobsDone(Base):
    __tablename__ = '108_jobs_done'

    id = Column(INTEGER(11), primary_key=True)
    customerID = Column(INTEGER(11))
    createDate = Column(TIMESTAMP, server_default=text("current_timestamp()"))


class 108Lineproduct(Base):
    __tablename__ = '108_lineproduct'

    id = Column(INTEGER(11), primary_key=True)
    lineProductName = Column(String(100), nullable=False)
    img = Column(String(100))
    sectionID = Column(INTEGER(11), nullable=False)
    userID = Column(INTEGER(11), nullable=False)
    lineProductCreateDate = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))


class 108Linetoken(Base):
    __tablename__ = '108_linetoken'

    id = Column(INTEGER(11), primary_key=True)
    token = Column(String(256), nullable=False)
    userID = Column(INTEGER(11), nullable=False)
    groupDesc = Column(String(100), nullable=False)
    memberofGroup = Column(String(200))
    deleteStatus = Column(Enum('Y', 'N'), server_default=text("'N'"))
    createDatetime = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))


class 108Machine(Base):
    __tablename__ = '108_machine'

    id = Column(INTEGER(11), primary_key=True)
    machineName = Column(String(100), nullable=False)
    lineproductID = Column(INTEGER(11), nullable=False)
    userID = Column(INTEGER(11), nullable=False)
    machineCreateDate = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))


class 108Membertype(Base):
    __tablename__ = '108_membertype'

    id = Column(INTEGER(11), primary_key=True)
    memberCode = Column(String(50), nullable=False)
    memberDesc = Column(String(100), nullable=False)
    sboxLimit = Column(TINYINT(3), nullable=False)
    tagLimit = Column(TINYINT(3), nullable=False)
    widgetLimit = Column(TINYINT(3), nullable=False)
    dataLimit = Column(TINYINT(3), nullable=False)


class 108Rawdatum(Base):
    __tablename__ = '108_rawdata'

    id = Column(INTEGER(11), primary_key=True)
    data = Column(LONGTEXT, nullable=False)
    dateCreate = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"))
    dataof = Column(Enum('0', '1'), nullable=False)


class 108RawdataFull(Base):
    __tablename__ = '108_rawdata_full'

    id = Column(INTEGER(11), primary_key=True)
    data = Column(Text)


class 108ReportStatu(Base):
    __tablename__ = '108_report_status'

    id = Column(INTEGER(11), primary_key=True)
    sboxName = Column(String(21), nullable=False, index=True)
    statusValue = Column(INTEGER(2), nullable=False)
    userID = Column(INTEGER(11), nullable=False, index=True)
    datetimeStamp = Column(String(15), nullable=False, index=True)
    timeStampLocal = Column(DateTime, nullable=False)
    dateStamp = Column(Date, nullable=False, index=True)
    timeStamp = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))


class 108ReportTrande(Base):
    __tablename__ = '108_report_trande'

    id = Column(INTEGER(11), primary_key=True)
    userID = Column(INTEGER(11), nullable=False, index=True)
    datetimeStamp = Column(String(15), nullable=False, index=True)
    dateStamp = Column(Date, nullable=False)
    sboxName = Column(String(21), nullable=False, index=True)
    tagValue = Column(LONGTEXT, nullable=False)
    timeStamp = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))


class 108ReportUph(Base):
    __tablename__ = '108_report_uph'

    id = Column(INTEGER(11), primary_key=True)
    sboxName = Column(String(21), nullable=False, index=True)
    datetimeStamp = Column(String(15), nullable=False, index=True)
    dateStamp = Column(Date, nullable=False, index=True)
    userID = Column(INTEGER(11), nullable=False, index=True)
    dataUPH = Column(LONGTEXT, nullable=False)
    timeStamp = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))



class 108SboxFactoryPin(Base):
    __tablename__ = '108_sbox_factory_pin'

    id = Column(INTEGER(11), primary_key=True)
    sboxID = Column(INTEGER(11), nullable=False)
    assetID = Column(INTEGER(11), nullable=False, index=True)
    sectionID = Column(INTEGER(11), nullable=False)
    lineID = Column(INTEGER(11), nullable=False)
    machineID = Column(INTEGER(11), nullable=False)
    userID = Column(INTEGER(11), nullable=False, index=True)
    linkSection = Column(String(200))
    sboxAgent = Column(INTEGER(11))
    leftPosition = Column(Float, nullable=False)
    topPosition = Column(Float, nullable=False)
    sboxShow = Column(Enum('Y', 'N'), server_default=text("'N'"))


class 108SboxInfoMqtt(Base):
    __tablename__ = '108_sbox_info_mqtt'

    id = Column(INTEGER(11), primary_key=True)
    sboxpinpositionID = Column(INTEGER(11), index=True)
    assetID = Column(INTEGER(11), index=True)
    pinIndex = Column(INTEGER(11))
    mqttIndex = Column(INTEGER(2))
    sboxID = Column(INTEGER(11), index=True)
    userID = Column(INTEGER(11), index=True)
    mqttShow = Column(Enum('Y', 'N'), server_default=text("'N'"))


class 108SboxMachineHistory(Base):
    __tablename__ = '108_sbox_machine_history'

    id = Column(INTEGER(11), primary_key=True)
    oldMachineID = Column(INTEGER(11), nullable=False)
    newMachineID = Column(INTEGER(11), nullable=False)
    sboxID = Column(INTEGER(11), nullable=False)
    userID = Column(INTEGER(11), nullable=False)
    createDate = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"))


class 108SboxPinPosition(Base):
    __tablename__ = '108_sbox_pin_position'

    id = Column(INTEGER(11), primary_key=True)
    sboxID = Column(INTEGER(11), index=True)
    assetID = Column(INTEGER(11))
    userID = Column(INTEGER(11), index=True)
    leftPosition = Column(Float)
    topPosition = Column(Float)
    sboxShow = Column(Enum('Y', 'N'), nullable=False, server_default=text("'Y'"))


class 108SboxPinSubPosition(Base):
    __tablename__ = '108_sbox_pin_sub_position'

    id = Column(INTEGER(11), primary_key=True)
    sboxpinpositionID = Column(INTEGER(11))
    assetID = Column(INTEGER(11))
    pinIndex = Column(INTEGER(11))
    mqttIndex = Column(INTEGER(2))
    sboxID = Column(INTEGER(11), index=True)
    userID = Column(INTEGER(11), index=True)
    leftPosition = Column(Float)
    topPosition = Column(Float)
    pinShow = Column(Enum('Y', 'N'), nullable=False, server_default=text("'N'"))
    mqttShow = Column(Enum('Y', 'N'), server_default=text("'Y'"))


class 108SboxPinSubPositionMultimap(Base):
    __tablename__ = '108_sbox_pin_sub_position_multimap'

    id = Column(INTEGER(11), primary_key=True)
    sboxpinpositionID = Column(INTEGER(11))
    assetID = Column(INTEGER(11))
    pinIndex = Column(INTEGER(11))
    mqttIndex = Column(INTEGER(2))
    sboxID = Column(INTEGER(11), index=True)
    userID = Column(INTEGER(11), index=True)
    pinShow = Column(Enum('Y', 'N'), nullable=False, server_default=text("'N'"))
    mqttShow = Column(Enum('Y', 'N'), server_default=text("'Y'"))


class 108SboxSectionPin(Base):
    __tablename__ = '108_sbox_section_pin'

    id = Column(INTEGER(11), primary_key=True)
    sboxID = Column(INTEGER(11), nullable=False)
    machineID = Column(INTEGER(11), nullable=False, index=True)
    lineID = Column(INTEGER(11), nullable=False, index=True)
    sectionID = Column(INTEGER(11), nullable=False, index=True)
    userID = Column(INTEGER(11), nullable=False, index=True)
    linkLine = Column(String(200))
    sboxAgent = Column(INTEGER(11))
    leftPosition = Column(Float, nullable=False)
    topPosition = Column(Float, nullable=False)
    sboxShow = Column(Enum('Y', 'N'), server_default=text("'N'"))


class 108SboxTagStatu(Base):
    __tablename__ = '108_sbox_tag_status'

    id = Column(INTEGER(11), primary_key=True)
    statusName = Column(String(40), nullable=False)
    colorCode = Column(String(10), nullable=False)
    statusVal = Column(String(30), nullable=False)


class 108SboxType(Base):
    __tablename__ = '108_sbox_type'

    id = Column(INTEGER(11), primary_key=True)
    sboxType = Column(String(50), nullable=False)
    typeCode = Column(String(6), nullable=False)
    widgetMember = Column(TEXT, nullable=False)


class 108SboxUserWidget(Base):
    __tablename__ = '108_sbox_user_widget'

    id = Column(INTEGER(11), primary_key=True)
    sboxID = Column(INTEGER(11), nullable=False)
    widgetID = Column(INTEGER(11), nullable=False)
    userID = Column(INTEGER(11), nullable=False)
    datetimeCreate = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"))


class 108SboxVdostreaming(Base):
    __tablename__ = '108_sbox_vdostreaming'

    id = Column(INTEGER(11), primary_key=True)
    sboxID = Column(INTEGER(11))
    vdoLink = Column(String(255))
    vdoShow = Column(Enum('Y', 'N'), server_default=text("'N'"))
    userID = Column(INTEGER(11))


class 108SboxVirtual(Base):
    __tablename__ = '108_sbox_virtual'

    id = Column(INTEGER(11), primary_key=True)
    serialKey = Column(String(20))
    virtualsBox = Column(String(256))
    userID = Column(INTEGER(11))


class 108SboxVirtualkey(Base):
    __tablename__ = '108_sbox_virtualkey'

    id = Column(INTEGER(11), primary_key=True)
    serial = Column(String(100), nullable=False)
    num_virtualkey = Column(INTEGER(11), nullable=False)
    date_create = Column('date create', TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))


class 108Section(Base):
    __tablename__ = '108_section'

    id = Column(INTEGER(11), primary_key=True)
    sectionName = Column(String(50), nullable=False)
    img = Column(String(100))
    assetID = Column(INTEGER(11), nullable=False)
    userID = Column(INTEGER(11), nullable=False)
    sectionCreateDate = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"))


class 108Serialkey(Base):
    __tablename__ = '108_serialkey'

    id = Column(INTEGER(11), primary_key=True)
    serialKey = Column(String(20))
    virtualKey = Column(LONGTEXT)


class 108Tag(Base):
    __tablename__ = '108_tags'

    id = Column(INTEGER(11), primary_key=True)
    userID = Column(INTEGER(11), nullable=False)
    sboxType = Column(INTEGER(11), nullable=False)
    tagData = Column(String(29))
    tagInfo = Column(String(14))


class 108TagsDesc(Base):
    __tablename__ = '108_tags_desc'

    id = Column(INTEGER(11), primary_key=True)
    sboxtypeID = Column(INTEGER(11), nullable=False)
    tag = Column(INTEGER(11), nullable=False)
    tagDesc = Column(String(50), nullable=False)
    tagType = Column(Enum('data', 'info'))


class 108Tagtype(Base):
    __tablename__ = '108_tagtype'

    id = Column(INTEGER(11), primary_key=True)
    tagType = Column(String(50), nullable=False)


class 108Testval(Base):
    __tablename__ = '108_testval'

    id = Column(INTEGER(11), primary_key=True)
    val = Column(Text)


class 108TimeStamp(Base):
    __tablename__ = '108_time_stamp'

    id = Column(INTEGER(11), primary_key=True)
    serialKey = Column(String(20))
    realTime = Column(TIMESTAMP, server_default=text("current_timestamp()"))
    realTimeData = Column(TIMESTAMP, server_default=text("current_timestamp()"))
    sboxstatus = Column(String(2))
    realTimeDataRestore = Column(DateTime)


class 108UploadCsvLog(Base):
    __tablename__ = '108_upload_csv_log'

    id = Column(INTEGER(11), primary_key=True)
    csv_filename = Column(String(40), nullable=False)
    uploadTime = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    sizefile = Column(String(10), nullable=False)


class 108User(Base):
    __tablename__ = '108_user'

    id = Column(INTEGER(11), primary_key=True)
    username = Column(String(20), nullable=False)
    password = Column(String(255), nullable=False)
    fullname = Column(String(20))
    email = Column(String(100))
    mobile = Column(String(22))
    picture = Column(String(255))
    tagActive = Column(Enum('YES', 'NO'), nullable=False, server_default=text("'NO'"))
    memberType = Column(INTEGER(11), nullable=False, server_default=text("1"))
    customerID = Column(INTEGER(11))
    userCreateDate = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"))
    tmpcode = Column(String(6))


class 108UserWidget(Base):
    __tablename__ = '108_user_widget'

    id = Column(INTEGER(11), primary_key=True)
    widgetID = Column(INTEGER(11))
    userID = Column(INTEGER(11))
    sboxID = Column(INTEGER(11))
    tagVal = Column(String(100))
    widgetCreateDate = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"))


t__108_view_report_status = Table(
    '108_view_report_status', metadata,
    Column('id', INTEGER(11), server_default=text("'0'")),
    Column('sboxName', String(21)),
    Column('statusValue', INTEGER(2)),
    Column('userID', INTEGER(11)),
    Column('datetimeStamp', String(15)),
    Column('timeStampLocal', DateTime),
    Column('dateStamp', Date),
    Column('timeStamp', TIMESTAMP, server_default=text("'current_timestamp()'"))
)


t__108_view_sbox_asset = Table(
    '108_view_sbox_asset', metadata,
    Column('sboxid', INTEGER(11), server_default=text("'0'")),
    Column('mid', INTEGER(11), server_default=text("'0'")),
    Column('lid', INTEGER(11), server_default=text("'0'")),
    Column('sid', INTEGER(11), server_default=text("'0'")),
    Column('aid', INTEGER(11), server_default=text("'0'")),
    Column('serialKey', String(20)),
    Column('sboxtypeID', INTEGER(11)),
    Column('sboxName', String(50)),
    Column('factoryType', INTEGER(11)),
    Column('sboxReady', Enum('Y', 'N'), server_default=text("'N'")),
    Column('machineName', String(100)),
    Column('lineproductName', String(100)),
    Column('sectionName', String(50)),
    Column('assetName', String(100)),
    Column('img', String(100)),
    Column('userID', INTEGER(11))
)


t__108_view_sbox_line_alert = Table(
    '108_view_sbox_line_alert', metadata,
    Column('aid', INTEGER(11), server_default=text("'0'")),
    Column('mid', INTEGER(11), server_default=text("'0'")),
    Column('msg', String(256)),
    Column('msgShort', String(30)),
    Column('msg_Man', String(256)),
    Column('msgShort_Man', String(30)),
    Column('lid', INTEGER(11), server_default=text("'0'")),
    Column('token', String(256)),
    Column('sid', INTEGER(11), server_default=text("'0'")),
    Column('serialkey', String(20)),
    Column('monitor', Enum('sBoxtag', 'sBoxstatus')),
    Column('status_condition', String(10)),
    Column('tag', String(30)),
    Column('vmin', Float),
    Column('vmax', Float),
    Column('vfreq', INTEGER(11)),
    Column('vfreq_Man', INTEGER(11), server_default=text("'0'")),
    Column('vnum', INTEGER(11), server_default=text("'0'")),
    Column('alertday', String(50)),
    Column('alertstatus', Enum('active', '')),
    Column('sboxName', String(50)),
    Column('machineName', String(100))
)


t__108_view_sbox_line_alert_man = Table(
    '108_view_sbox_line_alert_man', metadata,
    Column('aid', INTEGER(11), server_default=text("'0'")),
    Column('mid', INTEGER(11), server_default=text("'0'")),
    Column('msg', String(256)),
    Column('msgShort', String(30)),
    Column('msg_Man', String(256)),
    Column('msgShort_Man', String(30)),
    Column('lid', INTEGER(11), server_default=text("'0'")),
    Column('token', String(256)),
    Column('sid', INTEGER(11), server_default=text("'0'")),
    Column('serialkey', String(20)),
    Column('monitor', Enum('sBoxtag', 'sBoxstatus')),
    Column('status_condition', String(10)),
    Column('tag', String(30)),
    Column('vmin', Float),
    Column('vmax', Float),
    Column('vfreq', INTEGER(11)),
    Column('vfreq_Man', INTEGER(11), server_default=text("'0'")),
    Column('vnum', INTEGER(11), server_default=text("'0'")),
    Column('alertday', String(50)),
    Column('alertstatus', Enum('active', '')),
    Column('sboxName', String(50)),
    Column('machineName', String(100))
)


t__108_view_sbox_type = Table(
    '108_view_sbox_type', metadata,
    Column('sid', INTEGER(11), server_default=text("'0'")),
    Column('serialKey', String(20)),
    Column('sboxName', String(50)),
    Column('sboxType', String(50)),
    Column('widgetMember', Text),
    Column('sboxtypeID', INTEGER(11), server_default=text("'0'")),
    Column('factoryType', String(20))
)


class 108VirtualsBoxSetting(Base):
    __tablename__ = '108_virtualsBox_setting'

    id = Column(INTEGER(11), primary_key=True)
    numVirtualsBox = Column(INTEGER(11))
    tagStart = Column(INTEGER(11))
    numInfoData = Column(INTEGER(11))


class 108Widget(Base):
    __tablename__ = '108_widget'

    id = Column(INTEGER(11), primary_key=True)
    widgetName = Column(String(20))
    widgetType = Column(Enum('Single', 'Multi'))


class OLD108RawdataJson(Base):
    __tablename__ = 'OLD_108_rawdata_json'

    id = Column(INTEGER(11), primary_key=True)
    json_data = Column(LONGTEXT, nullable=False)


class OLD108SboxPowermeterPinPosition(Base):
    __tablename__ = 'OLD_108_sbox_powermeter_pin_position'

    id = Column(INTEGER(11), primary_key=True)
    sboxID = Column(INTEGER(11))
    sboxSubID = Column(INTEGER(11))
    assetID = Column(INTEGER(11))
    userID = Column(INTEGER(11))
    leftPosition = Column(Float)
    topPosition = Column(Float)
    sboxShow = Column(Enum('Y', 'N'), nullable=False, server_default=text("'N'"))
    mqttShow = Column(String(100))


class OLD108SboxStatu(Base):
    __tablename__ = 'OLD_108_sbox_status'

    id = Column(INTEGER(11), primary_key=True)
    serialKey = Column(String(20), nullable=False)
    countTime = Column(INTEGER(11), nullable=False, server_default=text("0"))
    Other = Column(INTEGER(11), nullable=False, server_default=text("0"))
    OtherStop = Column(INTEGER(11), nullable=False, server_default=text("0"))
    MachineStop = Column(INTEGER(11), nullable=False, server_default=text("0"))
    Setting = Column(INTEGER(11), nullable=False, server_default=text("0"))
    StopPlan = Column(INTEGER(11), nullable=False, server_default=text("0"))
    Runing = Column(INTEGER(11), nullable=False, server_default=text("0"))
    NoIdentify = Column(INTEGER(11), nullable=False, server_default=text("0"))
    updateDatetime = Column(DateTime)


class OLD108WidgetTmp(Base):
    __tablename__ = 'OLD_108_widget_tmp'

    id = Column(INTEGER(11), primary_key=True)
    widgetName = Column(String(50), nullable=False)
    widgetType = Column(INTEGER(11), nullable=False)
    widgetImage = Column(String(50), nullable=False)
    multiPosition = Column(Enum('Y', 'N'), nullable=False)
