# -*- coding: utf-8 -*-  # 核心：声明文件编码为 UTF-8
"""
婚介信息管理系统 - 后端API
技术栈: Python FastAPI + SQLite
"""
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from pathlib import Path
import sqlite3
import uuid
from datetime import datetime

app = FastAPI(title="丽姐·锦绣谱", version="2.0.0")

# CORS 配置 - 允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件配置 - 上传的图片
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# 数据库配置
DATABASE = "marriage.db"


def get_db():
    """获取数据库连接"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """初始化数据库表"""
    conn = get_db()
    cursor = conn.cursor()
    # 创建会员表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_no TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            gender TEXT NOT NULL,
            age INTEGER NOT NULL,
            education TEXT NOT NULL,
            occupation TEXT NOT NULL,
            marital_status TEXT NOT NULL,
            hukou_location TEXT NOT NULL,
            current_residence TEXT NOT NULL,
            contact TEXT NOT NULL,
            height INTEGER,
            income TEXT,
            partner_requirement TEXT,
            registration_time TEXT NOT NULL,
            remark TEXT,
            zodiac TEXT NOT NULL,
            personality TEXT,
            family_members TEXT,
            property TEXT,
            photos TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # 创建用户表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # 添加默认管理员用户（密码：admin123）
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "admin123"))
    
    # 创建菜单表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS menus (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            path TEXT NOT NULL,
            icon TEXT,
            parent_id INTEGER DEFAULT 0,
            sort_order INTEGER DEFAULT 0,
            is_visible INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 创建角色表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 创建用户角色关联表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_roles (
            user_id INTEGER,
            role_id INTEGER,
            PRIMARY KEY (user_id, role_id)
        )
    """)
    
    # 创建角色菜单权限表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS role_menus (
            role_id INTEGER,
            menu_id INTEGER,
            PRIMARY KEY (role_id, menu_id)
        )
    """)
    
    # 初始化默认数据
    # 创建admin角色
    cursor.execute("SELECT COUNT(*) FROM roles")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO roles (name, description) VALUES (?, ?)", ("admin", "管理员"))
        
        # 创建默认菜单
        default_menus = [
            ("数据统计", "/dashboard", "DataAnalysis", 1),
            ("会员管理", "/members", "User", 2),
            ("用户管理", "/users", "UserFilled", 3),
            ("菜单管理", "/menus", "Menu", 4),
            ("角色管理", "/roles", "Stamp", 5),
        ]
        cursor.executemany("INSERT INTO menus (name, path, icon, sort_order) VALUES (?, ?, ?, ?)", default_menus)
        
        # 获取admin角色和菜单ID
        cursor.execute("SELECT id FROM roles WHERE name = ?", ("admin",))
        admin_role_id = cursor.fetchone()["id"]
        
        # 给admin角色分配所有菜单权限
        cursor.execute("SELECT id FROM menus")
        menu_ids = [row["id"] for row in cursor.fetchall()]
        for menu_id in menu_ids:
            cursor.execute("INSERT INTO role_menus (role_id, menu_id) VALUES (?, ?)", (admin_role_id, menu_id))
        
        # 给admin用户分配admin角色
        cursor.execute("SELECT id FROM users WHERE username = ?", ("admin",))
        admin_user = cursor.fetchone()
        if admin_user:
            cursor.execute("INSERT INTO user_roles (user_id, role_id) VALUES (?, ?)", (admin_user["id"], admin_role_id))
    
    conn.commit()
    conn.close()


# 数据模型
class MemberCreate(BaseModel):
    """新增会员请求模型"""
    name: str = Field(..., min_length=1, max_length=50, description="姓名")
    gender: str = Field(..., description="性别")
    age: int = Field(..., ge=18, le=100, description="年龄")
    education: str = Field(..., description="学历")
    occupation: str = Field(..., min_length=1, max_length=100, description="职业")
    marital_status: str = Field(..., description="婚姻状况")
    hukou_location: str = Field(..., min_length=1, max_length=200, description="户籍所在地")
    current_residence: str = Field(..., min_length=1, max_length=200, description="现居住地")
    contact: str = Field(..., min_length=1, max_length=100, description="联系方式")
    height: Optional[int] = Field(None, ge=100, le=220, description="身高(cm)")
    income: Optional[str] = Field(None, max_length=50, description="收入")
    partner_requirement: Optional[str] = Field(None, description="择偶要求")
    remark: Optional[str] = Field(None, description="备注")
    zodiac: str = Field(..., description="生肖")
    personality: Optional[str] = Field(None, description="性格")
    family_members: Optional[str] = Field(None, description="家庭人员")
    property: Optional[str] = Field(None, description="房车情况")
    photos: Optional[str] = Field(None, description="照片，JSON数组")

    @field_validator('gender')
    @classmethod
    def validate_gender(cls, v):
        if v not in ['男', '女']:
            raise ValueError('性别必须是男或女')
        return v

    @field_validator('marital_status')
    @classmethod
    def validate_marital_status(cls, v):
        if v not in ['未婚', '离异', '丧偶']:
            raise ValueError('婚姻状况必须是未婚、离异或丧偶')
        return v

    @field_validator('education')
    @classmethod
    def validate_education(cls, v):
        valid_education = ['小学', '初中', '高中', '大专', '本科', '硕士', '博士']
        if v not in valid_education:
            raise ValueError(f'学历必须是{"、".join(valid_education)}之一')
        return v

    @field_validator('zodiac')
    @classmethod
    def validate_zodiac(cls, v):
        valid_zodiac = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪']
        if v not in valid_zodiac:
            raise ValueError(f'生肖必须是{"、".join(valid_zodiac)}之一')
        return v


class MemberResponse(BaseModel):
    """会员记录响应模型"""
    id: int
    member_no: str
    name: str
    gender: str
    age: int
    education: str
    occupation: str
    marital_status: str
    hukou_location: str
    current_residence: str
    contact: str
    height: Optional[int]
    income: Optional[str]
    partner_requirement: Optional[str]
    registration_time: str
    remark: Optional[str]
    zodiac: Optional[str]
    personality: Optional[str]
    family_members: Optional[str]
    property: Optional[str]
    photos: Optional[str]
    created_at: str


class PaginatedResponse(BaseModel):
    """分页响应模型"""
    items: List[MemberResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


# 用户相关模型
class UserCreate(BaseModel):
    """新增用户请求模型"""
    username: str = Field(..., min_length=2, max_length=20, description="登录名")
    password: str = Field(..., min_length=6, max_length=20, description="登录密码")

class UserResponse(BaseModel):
    """用户响应模型"""
    id: int
    username: str
    created_at: str
    updated_at: str


class BatchDeleteRequest(BaseModel):
    """批量删除请求模型"""
    ids: List[int] = Field(..., description="要删除的记录ID列表")

# API 路由
@app.on_event("startup")
def startup_event():
    """应用启动时初始化数据库"""
    init_db()


@app.get("/")
def root():
    """健康检查"""
    return {"status": "ok", "message": "婚介信息管理系统 API 运行中"}


@app.post("/api/members", response_model=MemberResponse)
def create_member(member: MemberCreate):
    """新增会员记录"""
    conn = get_db()
    cursor = conn.cursor()
    
    # 生成会员编号
    member_no = f"MEM{datetime.now().strftime('%Y%m%d%H%M%S')}{str(uuid.uuid4())[:4].upper()}"
    # 登记时间
    registration_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        cursor.execute("""
            INSERT INTO members 
            (member_no, name, gender, age, education, occupation, marital_status,
             hukou_location, current_residence, contact, height, income, 
             partner_requirement, registration_time, remark, zodiac, personality,
             family_members, property, photos)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            member_no,
            member.name,
            member.gender,
            member.age,
            member.education,
            member.occupation,
            member.marital_status,
            member.hukou_location,
            member.current_residence,
            member.contact,
            member.height,
            member.income,
            member.partner_requirement,
            registration_time,
            member.remark,
            member.zodiac,
            member.personality,
            member.family_members,
            member.property,
            member.photos
        ))
        conn.commit()
        
        # 获取插入的记录
        cursor.execute("SELECT * FROM members WHERE id = ?", (cursor.lastrowid,))
        row = cursor.fetchone()
        
        return MemberResponse(
            id=row["id"],
            member_no=row["member_no"],
            name=row["name"],
            gender=row["gender"],
            age=row["age"],
            education=row["education"],
            occupation=row["occupation"],
            marital_status=row["marital_status"],
            hukou_location=row["hukou_location"],
            current_residence=row["current_residence"],
            contact=row["contact"],
            height=row["height"],
            income=row["income"],
            partner_requirement=row["partner_requirement"],
            registration_time=row["registration_time"],
            remark=row["remark"],
            zodiac=row["zodiac"],
            personality=row["personality"],
            family_members=row["family_members"],
            property=row["property"],
            photos=row["photos"],
            created_at=row["created_at"]
        )
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


@app.get("/api/members", response_model=PaginatedResponse)
def get_members(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    gender: Optional[str] = Query(None, description="性别筛选"),
    marital_status: Optional[str] = Query(None, description="婚姻状况筛选"),
    age_min: Optional[int] = Query(None, ge=18, le=100, description="最小年龄"),
    age_max: Optional[int] = Query(None, ge=18, le=100, description="最大年龄"),
    education: Optional[str] = Query(None, description="学历筛选"),
    sort_field: Optional[str] = Query("created_at", description="排序字段"),
    sort_order: Optional[str] = Query("desc", description="排序方向")
):
    """获取会员列表（支持分页、搜索、筛选、排序）"""
    conn = get_db()
    cursor = conn.cursor()
    
    # 允许的排序字段
    allowed_sort_fields = ['created_at', 'age', 'name', 'registration_time']
    if sort_field not in allowed_sort_fields:
        sort_field = 'created_at'
    
    # 排序方向
    sort_order = "ASC" if sort_order == "asc" else "DESC"
    
    # 构建查询条件
    conditions = []
    params = []
    
    if search:
        conditions.append("(name LIKE ? OR occupation LIKE ? OR hukou_location LIKE ? OR current_residence LIKE ?)")
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%"])
    
    if gender:
        conditions.append("gender = ?")
        params.append(gender)
    
    if marital_status:
        conditions.append("marital_status = ?")
        params.append(marital_status)
    
    if age_min is not None:
        conditions.append("age >= ?")
        params.append(age_min)
    
    if age_max is not None:
        conditions.append("age <= ?")
        params.append(age_max)
    
    if education:
        conditions.append("education = ?")
        params.append(education)
    
    where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
    
    # 获取总数
    cursor.execute(f"SELECT COUNT(*) as total FROM members {where_clause}", params)
    total = cursor.fetchone()["total"]
    
    # 分页查询
    offset = (page - 1) * page_size
    cursor.execute(f"""
        SELECT * FROM members 
        {where_clause}
        ORDER BY {sort_field} {sort_order}
        LIMIT ? OFFSET ?
    """, params + [page_size, offset])
    
    rows = cursor.fetchall()
    conn.close()
    
    items = [
        MemberResponse(
            id=row["id"],
            member_no=row["member_no"],
            name=row["name"],
            gender=row["gender"],
            age=row["age"],
            education=row["education"],
            occupation=row["occupation"],
            marital_status=row["marital_status"],
            hukou_location=row["hukou_location"],
            current_residence=row["current_residence"],
            contact=row["contact"],
            height=row["height"],
            income=row["income"],
            partner_requirement=row["partner_requirement"],
            registration_time=row["registration_time"],
            remark=row["remark"],
            zodiac=row["zodiac"],
            personality=row["personality"],
            family_members=row["family_members"],
            property=row["property"],
            photos=row["photos"],
            created_at=row["created_at"]
        )
        for row in rows
    ]
    
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size if total > 0 else 1
    )


@app.get("/api/members/export")
def export_members(
    search: Optional[str] = Query(None, description="搜索关键词"),
    gender: Optional[str] = Query(None, description="性别筛选"),
    marital_status: Optional[str] = Query(None, description="婚姻状况筛选"),
    age_min: Optional[int] = Query(None, ge=18, le=100, description="最小年龄"),
    age_max: Optional[int] = Query(None, ge=18, le=100, description="最大年龄"),
    education: Optional[str] = Query(None, description="学历筛选")
):
    """导出会员数据（支持筛选条件）"""
    conn = get_db()
    cursor = conn.cursor()
    
    # 构建查询条件
    conditions = []
    params = []
    
    if search:
        conditions.append("(name LIKE ? OR occupation LIKE ? OR hukou_location LIKE ? OR current_residence LIKE ?)")
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%"])
    
    if gender:
        conditions.append("gender = ?")
        params.append(gender)
    
    if marital_status:
        conditions.append("marital_status = ?")
        params.append(marital_status)
    
    if age_min is not None:
        conditions.append("age >= ?")
        params.append(age_min)
    
    if age_max is not None:
        conditions.append("age <= ?")
        params.append(age_max)
    
    if education:
        conditions.append("education = ?")
        params.append(education)
    
    where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
    
    cursor.execute(f"""
        SELECT * FROM members 
        {where_clause}
        ORDER BY created_at DESC
    """, params)
    
    rows = cursor.fetchall()
    conn.close()
    
    # 转换为列表
    items = [
        {
            "member_no": row["member_no"],
            "name": row["name"],
            "gender": row["gender"],
            "age": row["age"],
            "education": row["education"],
            "occupation": row["occupation"],
            "marital_status": row["marital_status"],
            "hukou_location": row["hukou_location"],
            "current_residence": row["current_residence"],
            "contact": row["contact"],
            "height": row["height"] if row["height"] else "",
            "income": row["income"] if row["income"] else "",
            "partner_requirement": row["partner_requirement"] if row["partner_requirement"] else "",
            "registration_time": row["registration_time"],
            "remark": row["remark"] if row["remark"] else "",
            "zodiac": row["zodiac"] if row["zodiac"] else "",
            "personality": row["personality"] if row["personality"] else "",
            "family_members": row["family_members"] if row["family_members"] else "",
            "property": row["property"] if row["property"] else "",
            "photos": row["photos"] if row["photos"] else ""
        }
        for row in rows
    ]
    
    return {
        "total": len(items),
        "items": items
    }


@app.get("/api/members/{member_id}", response_model=MemberResponse)
def get_member(member_id: int):
    """获取单条会员记录"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members WHERE id = ?", (member_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="记录不存在")
    
    return MemberResponse(
        id=row["id"],
        member_no=row["member_no"],
        name=row["name"],
        gender=row["gender"],
        age=row["age"],
        education=row["education"],
        occupation=row["occupation"],
        marital_status=row["marital_status"],
        hukou_location=row["hukou_location"],
        current_residence=row["current_residence"],
        contact=row["contact"],
        height=row["height"],
        income=row["income"],
        partner_requirement=row["partner_requirement"],
        registration_time=row["registration_time"],
        remark=row["remark"],
        zodiac=row["zodiac"],
        personality=row["personality"],
        family_members=row["family_members"],
        property=row["property"],
        photos=row["photos"],
        created_at=row["created_at"]
    )


@app.put("/api/members/{member_id}", response_model=MemberResponse)
def update_member(member_id: int, member: MemberCreate):
    """更新会员记录"""
    conn = get_db()
    cursor = conn.cursor()
    
    # 检查记录是否存在
    cursor.execute("SELECT id FROM members WHERE id = ?", (member_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="记录不存在")
    
    try:
        cursor.execute("""
            UPDATE members 
            SET name = ?, gender = ?, age = ?, education = ?, occupation = ?, marital_status = ?,
                hukou_location = ?, current_residence = ?, contact = ?, height = ?, income = ?,
                partner_requirement = ?, remark = ?, zodiac = ?, personality = ?,
                family_members = ?, property = ?, photos = ?
            WHERE id = ?
        """, (
            member.name,
            member.gender,
            member.age,
            member.education,
            member.occupation,
            member.marital_status,
            member.hukou_location,
            member.current_residence,
            member.contact,
            member.height,
            member.income,
            member.partner_requirement,
            member.remark,
            member.zodiac,
            member.personality,
            member.family_members,
            member.property,
            member.photos,
            member_id
        ))
        conn.commit()
        
        # 获取更新后的记录
        cursor.execute("SELECT * FROM members WHERE id = ?", (member_id,))
        row = cursor.fetchone()
        
        return MemberResponse(
            id=row["id"],
            member_no=row["member_no"],
            name=row["name"],
            gender=row["gender"],
            age=row["age"],
            education=row["education"],
            occupation=row["occupation"],
            marital_status=row["marital_status"],
            hukou_location=row["hukou_location"],
            current_residence=row["current_residence"],
            contact=row["contact"],
            height=row["height"],
            income=row["income"],
            partner_requirement=row["partner_requirement"],
            registration_time=row["registration_time"],
            remark=row["remark"],
            zodiac=row["zodiac"],
            personality=row["personality"],
            family_members=row["family_members"],
            property=row["property"],
            photos=row["photos"],
            created_at=row["created_at"]
        )
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


@app.delete("/api/members/{member_id}")
def delete_member(member_id: int):
    """删除会员记录"""
    conn = get_db()
    cursor = conn.cursor()
    
    # 检查记录是否存在
    cursor.execute("SELECT id FROM members WHERE id = ?", (member_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="记录不存在")
    
    cursor.execute("DELETE FROM members WHERE id = ?", (member_id,))
    conn.commit()
    conn.close()
    
    return {"message": "删除成功"}


@app.post("/api/members/upload-photos")
async def upload_photos(request: Request):
    """上传会员照片"""
    try:
        # 获取上传的文件
        form = await request.form()
        files = form.getlist('photos')
        
        if not files:
            raise HTTPException(status_code=400, detail="没有上传文件")
        
        # 确保上传目录存在
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)
        
        urls = []
        for file in files:
            # 生成唯一文件名
            ext = Path(file.filename).suffix if file.filename else '.jpg'
            filename = f"{uuid.uuid4()}{ext}"
            file_path = upload_dir / filename
            
            # 保存文件
            content = await file.read()
            with open(file_path, "wb") as f:
                f.write(content)
            
            # 返回文件访问URL (开发环境使用后端服务器地址)
            urls.append(f"/uploads/{filename}")
        
        return JSONResponse(content={"urls": urls})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/members/batch-delete")
def batch_delete_members(request: BatchDeleteRequest):
    """批量删除会员记录"""
    if not request.ids:
        raise HTTPException(status_code=400, detail="删除ID列表不能为空")
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        # 构建IN查询的参数占位符
        placeholders = ",".join(["?"] * len(request.ids))
        # 检查记录是否存在
        cursor.execute(f"SELECT id FROM members WHERE id IN ({placeholders})", request.ids)
        existing_ids = [row["id"] for row in cursor.fetchall()]
        
        if len(existing_ids) == 0:
            conn.close()
            raise HTTPException(status_code=404, detail="没有找到要删除的记录")
        
        # 执行批量删除
        cursor.execute(f"DELETE FROM members WHERE id IN ({placeholders})", request.ids)
        deleted_count = cursor.rowcount
        conn.commit()
        
        return {
            "message": "批量删除成功",
            "deleted_count": deleted_count
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


# 统计接口
@app.get("/api/stats")
def get_stats():
    """获取统计信息"""
    conn = get_db()
    cursor = conn.cursor()
    
    # 总人数
    cursor.execute("SELECT COUNT(*) as total FROM members")
    total = cursor.fetchone()["total"]
    
    # 男女人数
    cursor.execute("SELECT gender, COUNT(*) as count FROM members GROUP BY gender")
    gender_stats = {row["gender"]: row["count"] for row in cursor.fetchall()}
    
    # 婚姻状况统计
    cursor.execute("SELECT marital_status, COUNT(*) as count FROM members GROUP BY marital_status")
    marital_stats = {row["marital_status"]: row["count"] for row in cursor.fetchall()}
    
    # 本月新增
    cursor.execute("""
        SELECT COUNT(*) as count FROM members 
        WHERE strftime('%Y-%m', created_at) = strftime('%Y-%m', 'now')
    """)
    this_month = cursor.fetchone()["count"]
    
    conn.close()
    
    return {
        "total": total,
        "male": gender_stats.get("男", 0),
        "female": gender_stats.get("女", 0),
        "unmarried": marital_stats.get("未婚", 0),
        "divorced": marital_stats.get("离异", 0),
        "widowed": marital_stats.get("丧偶", 0),
        "this_month": this_month
    }

# 用户角色分配模型
class UserRoleAssign(BaseModel):
    role_id: Optional[int] = None

# 用户管理接口
@app.get("/api/users")
def get_users():
    """获取用户列表（包含角色信息）"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users ORDER BY id")
    rows = cursor.fetchall()
    
    users_with_roles = []
    for row in rows:
        user_id = row["id"]
        # 查询用户角色
        cursor.execute("""
            SELECT r.* FROM roles r
            INNER JOIN user_roles ur ON r.id = ur.role_id
            WHERE ur.user_id = ?
        """, (user_id,))
        role_rows = cursor.fetchall()
        roles = [{
            "id": r["id"],
            "name": r["name"],
            "description": r["description"],
            "created_at": r["created_at"]
        } for r in role_rows]
        
        user_dict = {
            "id": row["id"],
            "username": row["username"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
            "roles": roles
        }
        users_with_roles.append(user_dict)
    
    conn.close()
    return users_with_roles

@app.post("/api/users", response_model=UserResponse)
def create_user(user: UserCreate):
    """新增用户"""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user.username, user.password))
        conn.commit()
        
        # 获取插入的记录
        cursor.execute("SELECT * FROM users WHERE id = ?", (cursor.lastrowid,))
        row = cursor.fetchone()
        
        return UserResponse(
            id=row["id"],
            username=row["username"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )
    except sqlite3.IntegrityError:
        conn.rollback()
        raise HTTPException(status_code=400, detail="用户名已存在")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.put("/api/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate):
    """更新用户"""
    conn = get_db()
    cursor = conn.cursor()
    
    # 检查记录是否存在
    cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="用户不存在")
    
    try:
        cursor.execute("UPDATE users SET username = ?, password = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", 
                      (user.username, user.password, user_id))
        conn.commit()
        
        # 获取更新后的记录
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        
        return UserResponse(
            id=row["id"],
            username=row["username"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )
    except sqlite3.IntegrityError:
        conn.rollback()
        raise HTTPException(status_code=400, detail="用户名已存在")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.delete("/api/users/{user_id}")
def delete_user(user_id: int):
    """删除用户"""
    conn = get_db()
    cursor = conn.cursor()
    
    # 检查记录是否存在
    cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 不允许删除最后一个用户
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 1:
        conn.close()
        raise HTTPException(status_code=400, detail="不能删除最后一个用户")
    
    # 删除用户角色关联
    cursor.execute("DELETE FROM user_roles WHERE user_id = ?", (user_id,))
    # 删除用户
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    
    return {"message": "删除成功"}


@app.post("/api/users/{user_id}/role")
def assign_user_role(user_id: int, data: UserRoleAssign):
    """分配角色给用户"""
    conn = get_db()
    cursor = conn.cursor()
    
    # 检查用户是否存在
    cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="用户不存在")
    
    try:
        # 删除旧的角色关联
        cursor.execute("DELETE FROM user_roles WHERE user_id = ?", (user_id,))
        
        # 如果指定了角色，添加新的角色关联
        if data.role_id:
            # 检查角色是否存在
            cursor.execute("SELECT id FROM roles WHERE id = ?", (data.role_id,))
            if not cursor.fetchone():
                conn.rollback()
                conn.close()
                raise HTTPException(status_code=404, detail="角色不存在")
            
            cursor.execute("INSERT INTO user_roles (user_id, role_id) VALUES (?, ?)", (user_id, data.role_id))
        
        conn.commit()
        return {"message": "分配角色成功"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# 角色模型
class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None

class RoleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: str

# 登录相关模型
class LoginRequest(BaseModel):
    """登录请求模型"""
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")

class LoginResponse(BaseModel):
    """登录响应模型"""
    success: bool
    message: str
    token: Optional[str] = None
    user: Optional[UserResponse] = None
    roles: Optional[List[RoleResponse]] = None
    menus: Optional[List[dict]] = None

# ========== 菜单管理 API ==========

# 菜单模型
class MenuCreate(BaseModel):
    name: str
    path: str
    icon: Optional[str] = None
    parent_id: int = 0
    sort_order: int = 0
    is_visible: bool = True

class MenuResponse(BaseModel):
    id: int
    name: str
    path: str
    icon: Optional[str]
    parent_id: int
    sort_order: int
    is_visible: int
    created_at: str
    children: Optional[List["MenuResponse"]] = None

# 角色菜单分配模型
class RoleMenuAssign(BaseModel):
    menu_ids: List[int]

def build_menu_tree(menus: List[dict], parent_id: int = 0) -> List[dict]:
    """构建菜单树形结构"""
    tree = []
    for menu in menus:
        if menu["parent_id"] == parent_id:
            children = build_menu_tree(menus, menu["id"])
            menu_dict = {
                "id": menu["id"],
                "name": menu["name"],
                "path": menu["path"],
                "icon": menu["icon"],
                "parent_id": menu["parent_id"],
                "sort_order": menu["sort_order"],
                "is_visible": menu["is_visible"],
                "created_at": menu["created_at"]
            }
            if children:
                menu_dict["children"] = children
            tree.append(menu_dict)
    return tree

@app.get("/api/menus", response_model=List[MenuResponse])
def get_menus():
    """获取所有菜单（树形结构）"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menus ORDER BY sort_order")
    rows = cursor.fetchall()
    conn.close()
    
    menus = [dict(row) for row in rows]
    tree = build_menu_tree(menus)
    return tree

@app.post("/api/menus", response_model=MenuResponse)
def create_menu(menu: MenuCreate):
    """新增菜单"""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO menus (name, path, icon, parent_id, sort_order, is_visible)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (menu.name, menu.path, menu.icon, menu.parent_id, menu.sort_order, 1 if menu.is_visible else 0))
        conn.commit()
        
        cursor.execute("SELECT * FROM menus WHERE id = ?", (cursor.lastrowid,))
        row = cursor.fetchone()
        
        return MenuResponse(
            id=row["id"],
            name=row["name"],
            path=row["path"],
            icon=row["icon"],
            parent_id=row["parent_id"],
            sort_order=row["sort_order"],
            is_visible=row["is_visible"],
            created_at=row["created_at"]
        )
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.put("/api/menus/{menu_id}", response_model=MenuResponse)
def update_menu(menu_id: int, menu: MenuCreate):
    """更新菜单"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM menus WHERE id = ?", (menu_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="菜单不存在")
    
    try:
        cursor.execute("""
            UPDATE menus 
            SET name = ?, path = ?, icon = ?, parent_id = ?, sort_order = ?, is_visible = ?
            WHERE id = ?
        """, (menu.name, menu.path, menu.icon, menu.parent_id, menu.sort_order, 1 if menu.is_visible else 0, menu_id))
        conn.commit()
        
        cursor.execute("SELECT * FROM menus WHERE id = ?", (menu_id,))
        row = cursor.fetchone()
        
        return MenuResponse(
            id=row["id"],
            name=row["name"],
            path=row["path"],
            icon=row["icon"],
            parent_id=row["parent_id"],
            sort_order=row["sort_order"],
            is_visible=row["is_visible"],
            created_at=row["created_at"]
        )
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.delete("/api/menus/{menu_id}")
def delete_menu(menu_id: int):
    """删除菜单"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM menus WHERE id = ?", (menu_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="菜单不存在")
    
    # 删除子菜单
    cursor.execute("DELETE FROM menus WHERE parent_id = ?", (menu_id,))
    # 删除菜单
    cursor.execute("DELETE FROM menus WHERE id = ?", (menu_id,))
    # 删除角色菜单权限
    cursor.execute("DELETE FROM role_menus WHERE menu_id = ?", (menu_id,))
    
    conn.commit()
    conn.close()
    
    return {"message": "删除成功"}

@app.get("/api/roles", response_model=List[RoleResponse])
def get_roles():
    """获取角色列表"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM roles ORDER BY id")
    rows = cursor.fetchall()
    conn.close()
    
    return [
        RoleResponse(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            created_at=row["created_at"]
        )
        for row in rows
    ]

@app.post("/api/roles", response_model=RoleResponse)
def create_role(role: RoleCreate):
    """新增角色"""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO roles (name, description) VALUES (?, ?)", (role.name, role.description))
        conn.commit()
        
        cursor.execute("SELECT * FROM roles WHERE id = ?", (cursor.lastrowid,))
        row = cursor.fetchone()
        
        return RoleResponse(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            created_at=row["created_at"]
        )
    except sqlite3.IntegrityError:
        conn.rollback()
        raise HTTPException(status_code=400, detail="角色名已存在")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.put("/api/roles/{role_id}", response_model=RoleResponse)
def update_role(role_id: int, role: RoleCreate):
    """更新角色"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM roles WHERE id = ?", (role_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="角色不存在")
    
    try:
        cursor.execute("UPDATE roles SET name = ?, description = ? WHERE id = ?", 
                      (role.name, role.description, role_id))
        conn.commit()
        
        cursor.execute("SELECT * FROM roles WHERE id = ?", (role_id,))
        row = cursor.fetchone()
        
        return RoleResponse(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            created_at=row["created_at"]
        )
    except sqlite3.IntegrityError:
        conn.rollback()
        raise HTTPException(status_code=400, detail="角色名已存在")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.delete("/api/roles/{role_id}")
def delete_role(role_id: int):
    """删除角色"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM roles WHERE id = ?", (role_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="角色不存在")
    
    # 删除角色菜单权限
    cursor.execute("DELETE FROM role_menus WHERE role_id = ?", (role_id,))
    # 删除用户角色关联
    cursor.execute("DELETE FROM user_roles WHERE role_id = ?", (role_id,))
    # 删除角色
    cursor.execute("DELETE FROM roles WHERE id = ?", (role_id,))
    
    conn.commit()
    conn.close()
    
    return {"message": "删除成功"}

@app.get("/api/roles/{role_id}/menus")
def get_role_menus(role_id: int):
    """获取角色菜单权限"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM roles WHERE id = ?", (role_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="角色不存在")
    
    cursor.execute("""
        SELECT m.* FROM menus m
        INNER JOIN role_menus rm ON m.id = rm.menu_id
        WHERE rm.role_id = ?
        ORDER BY m.sort_order
    """, (role_id,))
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

@app.put("/api/roles/{role_id}/menus")
def assign_role_menus(role_id: int, data: RoleMenuAssign):
    """分配菜单权限"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM roles WHERE id = ?", (role_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="角色不存在")
    
    try:
        # 删除旧的权限
        cursor.execute("DELETE FROM role_menus WHERE role_id = ?", (role_id,))
        
        # 添加新权限
        for menu_id in data.menu_ids:
            cursor.execute("INSERT INTO role_menus (role_id, menu_id) VALUES (?, ?)", (role_id, menu_id))
        
        conn.commit()
        return {"message": "分配成功"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# 登录接口
@app.post("/api/login", response_model=LoginResponse)
def login(login_data: LoginRequest):
    """用户登录"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (login_data.username, login_data.password))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return LoginResponse(
            success=False,
            message="用户名或密码错误"
        )
    
    user_id = row["id"]
    
    # 查询用户角色
    cursor.execute("""
        SELECT r.* FROM roles r
        INNER JOIN user_roles ur ON r.id = ur.role_id
        WHERE ur.user_id = ?
    """, (user_id,))
    role_rows = cursor.fetchall()
    roles = [RoleResponse(
        id=row["id"],
        name=row["name"],
        description=row["description"],
        created_at=row["created_at"]
    ) for row in role_rows]
    
    # 查询角色菜单权限
    menus = []
    if roles:
        role_ids = [r.id for r in roles]
        placeholders = ",".join(["?"] * len(role_ids))
        cursor.execute(f"""
            SELECT DISTINCT m.* FROM menus m
            INNER JOIN role_menus rm ON m.id = rm.menu_id
            WHERE rm.role_id IN ({placeholders})
            ORDER BY m.sort_order
        """, role_ids)
        menu_rows = cursor.fetchall()
        menus = [dict(row) for row in menu_rows]
    
    conn.close()
    
    return LoginResponse(
        success=True,
        message="登录成功",
        user=UserResponse(
            id=row["id"],
            username=row["username"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        ),
        roles=roles,
        menus=menus
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)