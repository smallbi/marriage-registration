"""
婚介信息管理系统 - 后端API
技术栈: Python FastAPI + SQLite
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
import sqlite3
import uuid
from datetime import datetime

app = FastAPI(title="婚介信息管理系统", version="2.0.0")

# CORS 配置 - 允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
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
    created_at: str


class PaginatedResponse(BaseModel):
    """分页响应模型"""
    items: List[MemberResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


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
             partner_requirement, registration_time, remark)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
            member.remark
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
            "remark": row["remark"] if row["remark"] else ""
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
                partner_requirement = ?, remark = ?
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)