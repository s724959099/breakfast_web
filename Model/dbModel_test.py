import datetime
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy import or_, and_, func
from sqlalchemy.orm import aliased

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:tmpr@twbp1@192.168.20.101:5432/Cloudesign"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class UserAccount(db.Model):
    __tablename__ = "UserAccount"
    UserId = db.Column(db.String(128), primary_key=True, nullable=False)
    CompanyId = db.Column(db.String(128), db.ForeignKey("Company.CompanyId"), nullable=True)
    Email = db.Column(db.String(128), unique=True, nullable=False)
    PasswordHash = db.Column(db.String(128), nullable=False)
    Name = db.Column(db.String(128), nullable=True)
    PictureUrl = db.Column(db.String(128), nullable=True)
    CreateDate = db.Column(db.DateTime(timezone=True), nullable=False)
    CreateBy = db.Column(db.String(128), nullable=False)
    ModifiedDate = db.Column(db.DateTime(timezone=True), nullable=True)
    ModifiedBy = db.Column(db.String(128), nullable=True)
    SoftDelete = db.Column(db.Boolean, nullable=False)

    def __init__(self,
                 UserId,
                 CompanyId,
                 Email,
                 PasswordHash,
                 Name,
                 PictureUrl=None,
                 ModifiedDate=None,
                 ModifiedBy=None,
                 SoftDelete=False):
        self.UserId = UserId
        self.CompanyId = CompanyId
        self.Email = Email
        self.PasswordHash = PasswordHash
        self.Name = Name
        self.PictureUrl = PictureUrl
        self.CreateDate = datetime.datetime.now()
        self.CreateBy = UserId
        self.ModifiedDate = ModifiedDate
        self.ModifiedBy = ModifiedBy
        self.SoftDelete = SoftDelete


class Tenant(db.Model):
    __tablename__ = "Tenant"

    TenantId = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    Name = db.Column(db.String(128), nullable=True, unique=True)  # unique
    CreateDate = db.Column(db.DateTime(timezone=True), nullable=False)
    CreateBy = db.Column(db.String(128), nullable=False)
    ModifiedDate = db.Column(db.DateTime(timezone=True), nullable=True)
    ModifiedBy = db.Column(db.String(128), nullable=True)
    SoftDelete = db.Column(db.Boolean, nullable=False)

    def __init__(self,
                 Name,
                 CreateBy,
                 ModifiedDate=None,
                 ModifiedBy=None,
                 SoftDelete=False,
                 ):
        self.Name = Name.lower()
        self.CreateDate = datetime.datetime.now()
        self.CreateBy = CreateBy
        self.ModifiedDate = ModifiedDate
        self.ModifiedBy = ModifiedBy
        self.SoftDelete = SoftDelete


class Company(db.Model):
    __tablename__ = "Company"

    CompanyId = db.Column(db.String(128), primary_key=True, nullable=False)
    TenantId = db.Column(db.Integer, db.ForeignKey("Tenant.TenantId"), nullable=False)
    """
    1:Design Company
    2:Custom Company
    """
    Type = db.Column(db.SMALLINT, nullable=False)
    Name = db.Column(db.String(128), nullable=False)
    CompanyStatus = db.Column(db.String(128), nullable=True)  # 公司狀態
    VATNumber = db.Column(db.String(128), nullable=False)  # 統一編號
    Capital = db.Column(db.Integer, nullable=True)  # 資本額
    PaidInCapital = db.Column(db.Integer, nullable=True)  # 實收資本額
    Owner = db.Column(db.String(128), nullable=True)  # 公司代表人
    Address = db.Column(db.String(128), nullable=True)
    RegistrationAuthority = db.Column(db.String(128), nullable=True)  # 登記機關
    ApprovedDate = db.Column(db.DateTime(timezone=True), nullable=True)  # 核准日期
    ChangeApprovedDate = db.Column(db.DateTime(timezone=True), nullable=True)  # 最後核准變更日期
    SiteUrl = db.Column(db.String(128), nullable=True)  # 官網
    Skype = db.Column(db.String(128), nullable=True)
    Phone = db.Column(db.String(128), nullable=True)
    Tel = db.Column(db.String(128), nullable=True)
    Email = db.Column(db.String(128), nullable=True)
    CreateDate = db.Column(db.DateTime(timezone=True), nullable=False)
    CreateBy = db.Column(db.String(128), nullable=False)
    ModifiedDate = db.Column(db.DateTime(timezone=True), nullable=True)
    ModifiedBy = db.Column(db.String(128), nullable=True)
    SoftDelete = db.Column(db.Boolean, nullable=False)

    def __init__(
            self,
            CompanyId,
            TenantId,
            Type,
            Name,
            VATNumber,
            Owner,
            CreateBy,
            CompanyStatus=None,
            Capital=None,
            PaidInCapital=None,
            Address=None,
            RegistrationAuthority=None,
            ApprovedDate=None,
            ChangeApprovedDate=None,
            SiteUrl=None,
            Skype=None,
            Phone=None,
            Tel=None,
            Email=None,
            ModifiedDate=None,
            ModifiedBy=None,
            SoftDelete=False,
    ):
        self.CompanyId = CompanyId
        self.TenantId = TenantId
        self.Type = Type
        self.Name = Name
        self.CompanyStatus = CompanyStatus
        self.VATNumber = VATNumber
        self.Capital = Capital
        self.PaidInCapital = PaidInCapital
        self.Owner = Owner
        self.Address = Address
        self.RegistrationAuthority = RegistrationAuthority
        self.ApprovedDate = ApprovedDate
        self.ChangeApprovedDate = ChangeApprovedDate
        self.SiteUrl = SiteUrl
        self.Skype = Skype
        self.Phone = Phone
        self.Tel = Tel
        self.Email = Email
        self.CreateDate = datetime.datetime.now()
        self.CreateBy = CreateBy
        self.ModifiedDate = ModifiedDate
        self.ModifiedBy = ModifiedBy
        self.SoftDelete = SoftDelete


class Transation(db.Model):
    __tablename__ = "Transation"
    TransationId = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    CompanyId = db.Column(db.String(128), db.ForeignKey("Company.CompanyId"), nullable=False)
    Type = db.Column(db.Boolean, nullable=False)
    Key = db.Column(db.String(128), nullable=True)
    CreateDate = db.Column(db.DateTime(timezone=True), nullable=False)
    CreateBy = db.Column(db.String(128), nullable=False)
    ModifiedDate = db.Column(db.DateTime(timezone=True), nullable=True)
    ModifiedBy = db.Column(db.String(128), nullable=True)
    SoftDelete = db.Column(db.Boolean, nullable=False)

    def __init__(
            self,
            TransationId,
            CompanyId,
            Type,
            Key
    ):
        self.TransationId = TransationId
        self.CompanyId = CompanyId
        self.Type = Type
        self.Key = Key
        self.CreateDate = datetime.datetime.now()
        self.CreateBy = CreateBy
        self.ModifiedDate = None
        self.ModifiedBy = None
        self.SoftDelete = False


class KeyStore(db.Model):
    __tablename__ = "KeyStore"
    KeyStoreId = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    TransationId = db.Column(db.Integer, db.ForeignKey("Transation.TransationId"), nullable=False)
    Key = db.Column(db.String(128), nullable=False)
    Order = db.Column(db.Boolean, nullable=False)
    CreateDate = db.Column(db.DateTime(timezone=True), nullable=False)
    CreateBy = db.Column(db.String(128), nullable=False)
    ModifiedDate = db.Column(db.DateTime(timezone=True), nullable=True)
    ModifiedBy = db.Column(db.String(128), nullable=True)
    SoftDelete = db.Column(db.Boolean, nullable=False)

    def __init__(
            self,
            KeyStoreId,
            TransationId,
            Key,
            Order
    ):
        self.KeyStoreId = KeyStoreId
        self.TransationId = TransationId
        self.Key = Key
        self.Order = Order
        self.CreateDate = datetime.datetime.now()
        self.CreateBy = CreateBy
        self.ModifiedDate = None
        self.ModifiedBy = None
        self.SoftDelete = False


class Service(db.Model):
    __tablename__ = "Service"
    ServiceId = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    ServiceNo = db.Column(db.String(128), nullable=False)
    CompanyId = db.Column(db.String(128), db.ForeignKey("Company.CompanyId"), nullable=False)
    Name = db.Column(db.String(128), nullable=False)
    Html = db.Column(db.TEXT, nullable=True)
    Price = db.Column(db.Integer, nullable=False)
    Type = db.Column(db.SMALLINT, nullable=False)
    PictureUrl = db.Column(db.String(128), nullable=True)
    ContractMonth = db.Column(db.Integer, nullable=True)
    CreateDate = db.Column(db.DateTime(timezone=True), nullable=False)
    CreateBy = db.Column(db.String(128), nullable=False)
    ModifiedDate = db.Column(db.DateTime(timezone=True), nullable=True)
    ModifiedBy = db.Column(db.String(128), nullable=True)
    SoftDelete = db.Column(db.Boolean, nullable=False)

    def __init__(
            self,
            ServiceNo,
            CompanyId,
            Name,
            Price,
            Type,
            CreateBy,
            Html=None,
            PictureUrl=None,
            ContractMonth=None,
    ):
        self.ServiceNo = ServiceNo
        self.CompanyId = CompanyId
        self.Name = Name
        self.Html = Html
        self.Price = Price
        self.Type = Type
        self.PictureUrl = PictureUrl
        self.ContractMonth = ContractMonth
        self.CreateBy = CreateBy

        self.CreateDate = datetime.datetime.now()
        self.ModifiedDate = None
        self.ModifiedBy = None
        self.SoftDelete = False


class ServiceCombination(db.Model):
    __tablename__ = "ServiceCombination"
    ServiceId = db.Column(db.Integer, primary_key=True, nullable=False)
    SubServiceId = db.Column(db.Integer, primary_key=True, nullable=False)
    Count = db.Column(db.Integer, nullable=False)
    CreateDate = db.Column(db.DateTime(timezone=True), nullable=False)
    CreateBy = db.Column(db.String(128), nullable=False)
    ModifiedDate = db.Column(db.DateTime(timezone=True), nullable=True)
    ModifiedBy = db.Column(db.String(128), nullable=True)
    SoftDelete = db.Column(db.Boolean, nullable=False)

    def __init__(
            self,
            ServiceId,
            SubServiceId,
            Count,
            CreateBy,
    ):
        self.ServiceId = ServiceId
        self.SubServiceId = SubServiceId
        self.Count = Count

        self.CreateBy = CreateBy
        self.CreateDate = datetime.datetime.now()
        self.ModifiedDate = None
        self.ModifiedBy = None
        self.SoftDelete = False


class SVHtmlPic(db.Model):
    __tablename__ = "SVHtmlPic"
    SVHtmlPicId = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    ServiceId = db.Column(db.Integer, db.ForeignKey("Service.ServiceId"), nullable=False)
    PicUrl = db.Column(db.String(256), nullable=False)
    Order = db.Column(db.Integer, nullable=False)
    CreateDate = db.Column(db.DateTime(timezone=True), nullable=False)
    CreateBy = db.Column(db.String(128), nullable=False)
    ModifiedDate = db.Column(db.DateTime(timezone=True), nullable=True)
    ModifiedBy = db.Column(db.String(128), nullable=True)
    SoftDelete = db.Column(db.Boolean, nullable=False)

    def __init__(
            self,
            ServiceId,
            PicUrl,
            Order,
            CreateBy,
    ):
        self.ServiceId = ServiceId
        self.PicUrl = PicUrl
        self.Order = Order
        self.CreateBy = CreateBy
        self.CreateDate = datetime.datetime.now()
        self.ModifiedDate = None
        self.ModifiedBy = None
        self.SoftDelete = False


class ServiceTag(db.Model):
    __tablename__ = "ServiceTag"
    ServiceId = db.Column(db.Integer, primary_key=True, nullable=False)
    TagId = db.Column(db.Integer, primary_key=True, nullable=False)
    CreateDate = db.Column(db.DateTime(timezone=True), nullable=False)
    CreateBy = db.Column(db.String(128), nullable=False)
    ModifiedDate = db.Column(db.DateTime(timezone=True), nullable=True)
    ModifiedBy = db.Column(db.String(128), nullable=True)
    SoftDelete = db.Column(db.Boolean, nullable=False)

    def __init__(self, ServiceId, TagId, CreateBy):
        self.ServiceId = ServiceId
        self.TagId = TagId
        self.CreateBy = CreateBy
        self.CreateDate = datetime.datetime.now()
        self.ModifiedDate = None
        self.ModifiedBy = None
        self.SoftDelete = False


class Tag(db.Model):
    __tablename__ = "Tag"
    TagId = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    TagNo = db.Column(db.String(128), nullable=False)
    CompanyId = db.Column(db.String(128), db.ForeignKey("Company.CompanyId"), nullable=False)
    Name = db.Column(db.String(128), nullable=False)
    Color = db.Column(db.Integer, nullable=False)  # 1~7
    CreateDate = db.Column(db.DateTime(timezone=True), nullable=False)
    CreateBy = db.Column(db.String(128), nullable=False)
    ModifiedDate = db.Column(db.DateTime(timezone=True), nullable=True)
    ModifiedBy = db.Column(db.String(128), nullable=True)
    SoftDelete = db.Column(db.Boolean, nullable=False)

    def __init__(
            self,
            TagNo,
            CompanyId,
            Name,
            Color,
            CreateBy,
            ModifiedDate=None,
            ModifiedBy=None,
            SoftDelete=False,
    ):
        self.TagNo = TagNo
        self.CompanyId = CompanyId
        self.Name = Name
        self.Color = Color
        self.CreateDate = datetime.datetime.now()
        self.CreateBy = CreateBy
        self.ModifiedDate = ModifiedDate
        self.ModifiedBy = ModifiedBy
        self.SoftDelete = SoftDelete


class Template(db.Model):
    __tablename__ = "Template"
    TemplateId = db.Column(db.Integer, db.ForeignKey("Template.TemplateId"), primary_key=True, nullable=False,
                           autoincrement=True)
    TemplateNo = db.Column(db.String(128), nullable=False)
    CompanyId = db.Column(db.String(128), db.ForeignKey("Company.CompanyId"), nullable=False)
    Name = db.Column(db.String(128), nullable=False)
    Description = db.Column(db.TEXT, nullable=True)
    CreateDate = db.Column(db.DateTime(timezone=True), nullable=False)
    CreateBy = db.Column(db.String(128), nullable=False)
    ModifiedDate = db.Column(db.DateTime(timezone=True), nullable=True)
    ModifiedBy = db.Column(db.String(128), nullable=True)
    SoftDelete = db.Column(db.Boolean, nullable=False)

    def __init__(
            self,
            TemplateNo,
            CompanyId,
            Name,
            Description,
            CreateBy,
            ModifiedDate=None,
            ModifiedBy=None,
            SoftDelete=False,
    ):
        self.TemplateNo = TemplateNo
        self.CompanyId = CompanyId
        self.Name = Name
        self.Description = Description
        self.CreateDate = datetime.datetime.now()
        self.CreateBy = CreateBy
        self.ModifiedDate = ModifiedDate
        self.ModifiedBy = ModifiedBy
        self.SoftDelete = SoftDelete


class SVTemplate(db.Model):
    __tablename__ = "SVTemplate"
    ServiceId = db.Column(db.Integer, primary_key=True, nullable=False)
    TemplateId = db.Column(db.Integer, primary_key=True, nullable=False)
    CreateDate = db.Column(db.DateTime(timezone=True), nullable=False)
    CreateBy = db.Column(db.String(128), nullable=False)
    ModifiedDate = db.Column(db.DateTime(timezone=True), nullable=True)
    ModifiedBy = db.Column(db.String(128), nullable=True)
    SoftDelete = db.Column(db.Boolean, nullable=False)

    def __init__(self, ServiceId, TemplateId, CreateBy):
        self.ServiceId = ServiceId
        self.TemplateId = TemplateId
        self.CreateBy = CreateBy
        self.CreateDate = datetime.datetime.now()
        self.ModifiedDate = None
        self.ModifiedBy = None
        self.SoftDelete = False


class TemplateItem(db.Model):
    __tablename__ = "TemplateItem"
    TemplateId = db.Column(db.Integer, primary_key=True, nullable=False)
    TemplateItemId = db.Column(db.Integer, primary_key=True, nullable=False)
    # 1:文字 2:款項
    Type = db.Column(db.Integer, nullable=False)
    Name = db.Column(db.String(128), nullable=False)
    StepDescription = db.Column(db.TEXT, nullable=True)
    PayPercent = db.Column(db.Integer, nullable=True)
    PushType = db.Column(db.Boolean, nullable=False)
    Order = db.Column(db.Integer, nullable=False)
    CreateDate = db.Column(db.DateTime(timezone=True), nullable=False)
    CreateBy = db.Column(db.String(128), nullable=False)
    ModifiedDate = db.Column(db.DateTime(timezone=True), nullable=True)
    ModifiedBy = db.Column(db.String(128), nullable=True)
    SoftDelete = db.Column(db.Boolean, nullable=False)

    def __init__(
            self,
            TemplateId,
            TemplateItemId,
            Type,
            Name,
            StepDescription,
            PushType,
            Order,
            CreateBy,
            PayPercent=None,
            ModifiedDate=None,
            ModifiedBy=None,
            SoftDelete=False,
    ):
        self.TemplateId = TemplateId
        self.TemplateItemId = TemplateItemId
        self.Type = Type
        self.Name = Name
        self.StepDescription = StepDescription
        self.PayPercent = PayPercent
        self.PushType = PushType
        self.Order = Order
        self.CreateDate = datetime.datetime.now()
        self.CreateBy = CreateBy
        self.ModifiedDate = ModifiedDate
        self.ModifiedBy = ModifiedBy
        self.SoftDelete = SoftDelete


class ProjectNotice(db.Model):
    __tablename__ = "ProjectNotice"
    ProjectId = db.Column(db.Integer, primary_key=True, nullable=False)
    ProjectNoticeId = db.Column(db.Integer, primary_key=True, nullable=False)
    CompanyId = db.Column(db.String(128), db.ForeignKey("Company.CompanyId"), nullable=False)
    Content = db.Column(db.String(256), nullable=False)
    Read = db.Column(db.Boolean, nullable=False)
    CreateDate = db.Column(db.DateTime(timezone=True), nullable=False)
    CreateBy = db.Column(db.String(128), nullable=False)
    ModifiedDate = db.Column(db.DateTime(timezone=True), nullable=True)
    ModifiedBy = db.Column(db.String(128), nullable=True)
    SoftDelete = db.Column(db.Boolean, nullable=False)

    def __init__(
            self,
            ProjectId,
            ProjectNoticeId,
            CompanyId,
            Content,
            Read,
            CreateBy
    ):
        self.ProjectId = ProjectId
        self.ProjectNoticeId = ProjectNoticeId
        self.CompanyId = CompanyId
        self.Content = Content
        self.Read = Read
        self.CreateDate = datetime.datetime.now()
        self.CreateBy = CreateBy
        self.ModifiedDate = None
        self.ModifiedBy = None
        self.SoftDelete = False


class ProjectMessage(db.Model):
    __tablename__ = "ProjectMessage"
    ProjectId = db.Column(db.Integer, primary_key=True, nullable=False)
    ProjectMessageId = db.Column(db.Integer, primary_key=True, nullable=False)
    CompanyId = db.Column(db.String(128), db.ForeignKey("Company.CompanyId"), nullable=False)
    Content = db.Column(db.TEXT, nullable=False)
    Read = db.Column(db.Boolean, nullable=False)
    CreateDate = db.Column(db.DateTime(timezone=True), nullable=False)
    CreateBy = db.Column(db.String(128), nullable=False)
    ModifiedDate = db.Column(db.DateTime(timezone=True), nullable=True)
    ModifiedBy = db.Column(db.String(128), nullable=True)
    SoftDelete = db.Column(db.Boolean, nullable=False)

    def __init__(
            self,
            ProjectId,
            ProjectMessageId,
            CompanyId,
            Content,
            Read,
            CreateBy
    ):
        self.ProjectId = ProjectId
        self.ProjectMessageId = ProjectMessageId
        self.CompanyId = CompanyId
        self.Content = Content
        self.Read = Read
        self.CreateDate = datetime.datetime.now()
        self.CreateBy = CreateBy
        self.ModifiedDate = None
        self.ModifiedBy = None
        self.SoftDelete = False


class ProjectLog(db.Model):
    __tablename__ = "ProjectLog"
    ProjectLogId = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    ProjectId = db.Column(db.Integer, db.ForeignKey("Project.ProjectId"), nullable=False)
    Name = db.Column(db.String(128), nullable=False)
    CreateDate = db.Column(db.DateTime(timezone=True), nullable=False)
    CreateBy = db.Column(db.String(128), nullable=False)
    ModifiedDate = db.Column(db.DateTime(timezone=True), nullable=True)
    ModifiedBy = db.Column(db.String(128), nullable=True)
    SoftDelete = db.Column(db.Boolean, nullable=False)

    def __init__(
            self,
            ProjectLogId,
            ProjectId,
            Name,
            CreateBy
    ):
        self.ProjectLogId = ProjectLogId
        self.ProjectId = ProjectId
        self.Name = Name
        self.CreateDate = datetime.datetime.now()
        self.CreateBy = CreateBy
        self.ModifiedDate = None
        self.ModifiedBy = None
        self.SoftDelete = False


class CommitFile(db.Model):
    __tablename__ = "CommitFile"
    CommitFileId = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    ProjectLogId = db.Column(db.Integer, db.ForeignKey("ProjectLog.ProjectLogId"), nullable=False)
    ProjectFileId = db.Column(db.Integer, db.ForeignKey("ProjectFile.ProjectFileId"), nullable=False)
    Status = db.Column(db.Boolean, nullable=False)
    CreateDate = db.Column(db.DateTime(timezone=True), nullable=False)
    CreateBy = db.Column(db.String(128), nullable=False)
    ModifiedDate = db.Column(db.DateTime(timezone=True), nullable=True)
    ModifiedBy = db.Column(db.String(128), nullable=True)
    SoftDelete = db.Column(db.Boolean, nullable=False)

    def __init__(
            self,
            CommitFileId,
            ProjectLogId,
            ProjectFileId,
            Status,
            CreateBy
    ):
        self.CommitFileId = CommitFileId
        self.ProjectLogId = ProjectLogId
        self.ProjectFileId = ProjectFileId
        self.Status = Status
        self.CreateDate = datetime.datetime.now()
        self.CreateBy = CreateBy
        self.ModifiedDate = None
        self.ModifiedBy = None
        self.SoftDelete = False


class ProjectFile(db.Model):
    __tablename__ = "ProjectFile"
    ProjectFileId = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    ProjectId = db.Column(db.Integer, db.ForeignKey("Project.ProjectId"), nullable=False)
    GroupId = db.Column(db.String(128), nullable=True)
    Name = db.Column(db.String(128), nullable=False)
    Format = db.Column(db.String(16), nullable=True)
    Type = db.Column(db.SMALLINT, nullable=False)
    Bytes = db.Column(db.Integer, nullable=False)
    Url = db.Column(db.String(256), nullable=False)
    CreateDate = db.Column(db.DateTime(timezone=True), nullable=False)
    CreateBy = db.Column(db.String(128), nullable=False)
    ModifiedDate = db.Column(db.DateTime(timezone=True), nullable=True)
    ModifiedBy = db.Column(db.String(128), nullable=True)
    SoftDelete = db.Column(db.Boolean, nullable=False)


class CommitFeedback(db.Model):
    __tablename__ = "CommitFeedback"
    CommitFeedbackId = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    CommitFileId = db.Column(db.Integer, db.ForeignKey("CommitFile.CommitFileId"), nullable=False)
    Content = db.Column(db.TEXT, nullable=False)
    CreateDate = db.Column(db.DateTime(timezone=True), nullable=False)
    CreateBy = db.Column(db.String(128), nullable=False)
    ModifiedDate = db.Column(db.DateTime(timezone=True), nullable=True)
    ModifiedBy = db.Column(db.String(128), nullable=True)
    SoftDelete = db.Column(db.Boolean, nullable=False)

    def __init__(
            self,
            CommitFeedbackId,
            CommitFileId,
            Content,
            CreateBy
    ):
        self.CommitFeedbackId = CommitFeedbackId
        self.CommitFileId = CommitFileId
        self.Content = Content
        self.CreateDate = datetime.datetime.now()
        self.CreateBy = CreateBy
        self.ModifiedDate = None
        self.ModifiedBy = None
        self.SoftDelete = False


class Order(db.Model):
    __tablename__ = "Order"
    OrderId = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    OrderNo = db.Column(db.String(128), nullable=False)
    ServiceId = db.Column(db.Integer, db.ForeignKey("Service.ServiceId"), nullable=False)
    CompanyId = db.Column(db.String(128), db.ForeignKey("Company.CompanyId"), nullable=False)
    TenantId = db.Column(db.Integer, db.ForeignKey("Tenant.TenantId"), nullable=False)
    Name = db.Column(db.String(128), nullable=False)
    Price = db.Column(db.Integer, nullable=False)
    Type = db.Column(db.SMALLINT, nullable=False)
    PictureUrl = db.Column(db.String(128), nullable=True)
    ContractMonth = db.Column(db.Integer, nullable=True)
    CreateDate = db.Column(db.DateTime(timezone=True), nullable=False)
    CreateBy = db.Column(db.String(128), nullable=False)
    ModifiedDate = db.Column(db.DateTime(timezone=True), nullable=True)
    ModifiedBy = db.Column(db.String(128), nullable=True)
    SoftDelete = db.Column(db.Boolean, nullable=False)

    def __init__(
            self,
            OrderNo,
            ServiceId,
            CompanyId,
            TenantId,
            Name,
            Price,
            Type,
            PictureUrl,
            ContractMonth,
            CreateBy
    ):
        self.OrderNo = OrderNo
        self.ServiceId = ServiceId
        self.CompanyId = CompanyId
        self.TenantId = TenantId
        self.Name = Name
        self.Price = Price
        self.Type = Type
        self.PictureUrl = PictureUrl
        self.ContractMonth = ContractMonth
        self.CreateDate = datetime.datetime.now()
        self.CreateBy = CreateBy
        self.ModifiedDate = None
        self.ModifiedBy = None
        self.SoftDelete = False


class OrderPaymentRecord(db.Model):
    __tablename__ = "OrderPaymentRecord"
    OrderId = db.Column(db.Integer, primary_key=True, nullable=False)
    OrderPaymentRecordId = db.Column(db.Integer, primary_key=True, nullable=False)
    OrderPaymentRecordNo = db.Column(db.String(128), nullable=False)
    BuyStatus = db.Column(db.SMALLINT, nullable=False)
    Remark = db.Column(db.String(256), nullable=True)
    Price = db.Column(db.Integer, nullable=False)
    Detail = db.Column(db.String(256), nullable=True)
    PayType = db.Column(db.SMALLINT, nullable=False)
    VAccount = db.Column(db.String(128), nullable=True)
    DeadLine = db.Column(db.DateTime(timezone=True), nullable=True)
    PayDate = db.Column(db.DateTime(timezone=True), nullable=True)
    CreateDate = db.Column(db.DateTime(timezone=True), nullable=False)
    CreateBy = db.Column(db.String(128), nullable=False)
    ModifiedDate = db.Column(db.DateTime(timezone=True), nullable=True)
    ModifiedBy = db.Column(db.String(128), nullable=True)
    SoftDelete = db.Column(db.Boolean, nullable=False)

    def __init__(
            self,
            OrderId,
            OrderPaymentRecordId,
            OrderPaymentRecordNo,
            BuyStatus,
            Remark,
            Detail,
            PayType,
            VAccount,
            Price,
            DeadLine,
            PayDate,
            CreateBy
    ):
        self.OrderId = OrderId
        self.OrderPaymentRecordId = OrderPaymentRecordId
        self.OrderPaymentRecordNo = OrderPaymentRecordNo
        self.BuyStatus = BuyStatus
        self.Remark = Remark
        self.Detail = Detail
        self.PayType = PayType
        self.VAccount = VAccount
        self.Price = Price
        self.DeadLine = DeadLine
        self.PayDate = PayDate
        self.CreateDate = datetime.datetime.now()
        self.CreateBy = CreateBy
        self.ModifiedDate = None
        self.ModifiedBy = None
        self.SoftDelete = False


class OrderItem(db.Model):
    __tablename__ = "OrderItem"
    OrderId = db.Column(db.Integer, primary_key=True, nullable=False)
    OrderItemId = db.Column(db.Integer, primary_key=True, nullable=False)
    Name = db.Column(db.String(128), nullable=False)
    PictureUrl = db.Column(db.String(128), nullable=True)
    Type = db.Column(db.Boolean, nullable=False)
    Count = db.Column(db.Integer, nullable=True)
    CreateDate = db.Column(db.DateTime(timezone=True), nullable=False)
    CreateBy = db.Column(db.String(128), nullable=False)
    ModifiedDate = db.Column(db.DateTime(timezone=True), nullable=True)
    ModifiedBy = db.Column(db.String(128), nullable=True)
    SoftDelete = db.Column(db.Boolean, nullable=False)

    def __init__(
            self,
            OrderId,
            OrderItemId,
            Name,
            PictureUrl,
            Type,
            Count,
            CreateBy
    ):
        self.OrderId = OrderId
        self.OrderItemId = OrderItemId
        self.Name = Name
        self.PictureUrl = PictureUrl
        self.Type = Type
        self.Count = Count
        self.CreateDate = datetime.datetime.now()
        self.CreateBy = CreateBy
        self.ModifiedDate = None
        self.ModifiedBy = None
        self.SoftDelete = False


class Right(db.Model):
    __tablename__ = "Right"
    RightId = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    RightNo = db.Column(db.String(128), nullable=False)
    OrderId = db.Column(db.Integer, db.ForeignKey("Order.OrderId"), nullable=False)
    Deadline = db.Column(db.DateTime(timezone=True), nullable=True)
    CreateDate = db.Column(db.DateTime(timezone=True), nullable=False)
    CreateBy = db.Column(db.String(128), nullable=False)
    ModifiedDate = db.Column(db.DateTime(timezone=True), nullable=True)
    ModifiedBy = db.Column(db.String(128), nullable=True)
    SoftDelete = db.Column(db.Boolean, nullable=False)

    def __init__(
            self,
            RightNo,
            OrderId,
            Deadline,
            CreateBy
    ):
        self.RightNo = RightNo
        self.OrderId = OrderId
        self.Deadline = Deadline
        self.CreateDate = datetime.datetime.now()
        self.CreateBy = CreateBy
        self.ModifiedDate = None
        self.ModifiedBy = None
        self.SoftDelete = False


class RightCombination(db.Model):
    __tablename__ = "RightCombination"
    RightId = db.Column(db.Integer, primary_key=True, nullable=False)
    OrderItemId = db.Column(db.Integer, primary_key=True, nullable=False)
    Count = db.Column(db.Integer, nullable=True)
    CreateDate = db.Column(db.DateTime(timezone=True), nullable=False)
    CreateBy = db.Column(db.String(128), nullable=False)
    ModifiedDate = db.Column(db.DateTime(timezone=True), nullable=True)
    ModifiedBy = db.Column(db.String(128), nullable=True)
    SoftDelete = db.Column(db.Boolean, nullable=False)

    def __init__(
            self,
            RightId,
            OrderItemId,
            Count,
            CreateBy
    ):
        self.RightId = RightId
        self.OrderItemId = OrderItemId
        self.Count = Count
        self.CreateDate = datetime.datetime.now()
        self.CreateBy = CreateBy
        self.ModifiedDate = None
        self.ModifiedBy = None
        self.SoftDelete = False


class Project(db.Model):
    __tablename__ = "Project"
    ProjectId = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    ProjectNo = db.Column(db.String(128), nullable=False)
    OrderId = db.Column(db.Integer, db.ForeignKey("Order.OrderId"), nullable=False)
    Demand = db.Column(db.TEXT, nullable=False)
    InProjectTemplateId = db.Column(db.Integer, nullable=False)
    Name = db.Column(db.String(128), nullable=False)
    CreateDate = db.Column(db.DateTime(timezone=True), nullable=False)
    CreateBy = db.Column(db.String(128), nullable=False)
    ModifiedDate = db.Column(db.DateTime(timezone=True), nullable=True)
    ModifiedBy = db.Column(db.String(128), nullable=True)
    SoftDelete = db.Column(db.Boolean, nullable=False)

    def __init__(
            self,
            ProjectNo,
            OrderId,
            Demand,
            CreateBy
    ):
        self.ProjectNo = ProjectNo
        self.OrderId = OrderId
        self.Demand = Demand
        self.InProjectTemplateId = InProjectTemplateId
        self.Name = Name
        self.CreateDate = datetime.datetime.now()
        self.CreateBy = CreateBy
        self.SoftDelete = False
        self.ModifiedDate = None
        self.ModifiedBy = None


class ProjectItem(db.Model):
    __tablename__ = "ProjectItem"
    ProjectId = db.Column(db.Integer, primary_key=True, nullable=False)
    ProjectItemId = db.Column(db.Integer, primary_key=True, nullable=False)
    Name = db.Column(db.String(128), nullable=False)
    Count = db.Column(db.Integer, nullable=False)
    CreateDate = db.Column(db.DateTime(timezone=True), nullable=False)
    CreateBy = db.Column(db.String(128), nullable=False)
    ModifiedDate = db.Column(db.DateTime(timezone=True), nullable=True)
    ModifiedBy = db.Column(db.String(128), nullable=True)
    SoftDelete = db.Column(db.Boolean, nullable=False)

    def __init__(
            self,
            ProjectId,
            ProjectItemId,
            Name,
            Count,
            CreateBy
    ):
        self.ProjectId = ProjectId
        self.ProjectItemId = ProjectItemId
        self.Name = Name
        self.Count = Count
        self.CreateDate = datetime.datetime.now()
        self.CreateBy = CreateBy
        self.ModifiedDate = None
        self.ModifiedBy = None
        self.SoftDelete = False


class ProjectTemplate(db.Model):
    __tablename__ = "ProjectTemplate"
    ProjectId = db.Column(db.Integer, primary_key=True, nullable=False)
    ProjectTemplateId = db.Column(db.Integer, primary_key=True, nullable=False)
    OrderPaymentRecordId = db.Column(db.Integer,
                                     nullable=True)  # db.ForeignKey("OrderPaymentRecord.OrderPaymentRecordId") code ForeignKey
    # there is no unique constraint matching given keys for referenced table "OrderPaymentRecord"
    Type = db.Column(db.SMALLINT, nullable=False)
    Name = db.Column(db.String(128), nullable=False)
    Order = db.Column(db.Integer, nullable=False)
    PushType = db.Column(db.Boolean, nullable=False)
    ExpectDate = db.Column(db.DateTime(timezone=True), nullable=False)
    CreateDate = db.Column(db.DateTime(timezone=True), nullable=False)
    CreateBy = db.Column(db.String(128), nullable=False)
    ModifiedDate = db.Column(db.DateTime(timezone=True), nullable=True)
    ModifiedBy = db.Column(db.String(128), nullable=True)
    SoftDelete = db.Column(db.Boolean, nullable=False)

    def __init__(
            self,
            ProjectId,
            ProjectTemplateId,
            OrderPaymentRecordId,
            Type,
            Name,
            Order,
            PushType,
            ExpectDate,
            CreateBy
    ):
        self.ProjectId = ProjectId
        self.ProjectTemplateId = ProjectTemplateId
        self.OrderPaymentRecordId = OrderPaymentRecordId
        self.Type = Type
        self.Name = Name
        self.Order = Order
        self.PushType = PushType
        self.ExpectDate = ExpectDate
        self.CreateDate = datetime.datetime.now()
        self.CreateBy = CreateBy
        self.ModifiedDate = None
        self.ModifiedBy = None
        self.SoftDelete = False


if __name__ == '__main__':
    manager.run()
