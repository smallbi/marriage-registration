// 模拟数据插入脚本
import fetch from 'node-fetch';

// 模拟数据
const mockData = [
  {
    name: '张三',
    gender: '男',
    age: 28,
    education: '本科',
    occupation: '软件工程师',
    marital_status: '未婚',
    hukou_location: '北京市朝阳区',
    current_residence: '北京市海淀区',
    contact: '13812345678',
    height: 175,
    income: '15k-20k',
    partner_requirement: '温柔善良，有稳定工作',
    remark: '性格开朗，喜欢运动'
  },
  {
    name: '李四',
    gender: '女',
    age: 25,
    education: '硕士',
    occupation: '教师',
    marital_status: '未婚',
    hukou_location: '上海市浦东新区',
    current_residence: '上海市静安区',
    contact: '13987654321',
    height: 165,
    income: '10k-15k',
    partner_requirement: '成熟稳重，有责任感',
    remark: '喜欢读书，旅行'
  },
  {
    name: '王五',
    gender: '男',
    age: 32,
    education: '大专',
    occupation: '销售经理',
    marital_status: '离异',
    hukou_location: '广州市天河区',
    current_residence: '广州市越秀区',
    contact: '13712345678',
    height: 180,
    income: '20k-25k',
    partner_requirement: '善解人意，能包容',
    remark: '有一个5岁的女儿'
  },
  {
    name: '赵六',
    gender: '女',
    age: 29,
    education: '本科',
    occupation: '医生',
    marital_status: '未婚',
    hukou_location: '深圳市南山区',
    current_residence: '深圳市福田区',
    contact: '13687654321',
    height: 168,
    income: '18k-22k',
    partner_requirement: '有爱心，责任心强',
    remark: '工作较忙，希望对方理解'
  },
  {
    name: '孙七',
    gender: '男',
    age: 35,
    education: '博士',
    occupation: '研究员',
    marital_status: '未婚',
    hukou_location: '杭州市西湖区',
    current_residence: '杭州市余杭区',
    contact: '13512345678',
    height: 172,
    income: '25k-30k',
    partner_requirement: '有共同语言，性格合拍',
    remark: '喜欢研究，偶尔运动'
  },
  {
    name: '周八',
    gender: '女',
    age: 26,
    education: '高中',
    occupation: '护士',
    marital_status: '未婚',
    hukou_location: '成都市锦江区',
    current_residence: '成都市武侯区',
    contact: '13487654321',
    height: 162,
    income: '8k-12k',
    partner_requirement: '体贴细心，有上进心',
    remark: '性格温柔，喜欢照顾人'
  },
  {
    name: '吴九',
    gender: '男',
    age: 30,
    education: '本科',
    occupation: '设计师',
    marital_status: '未婚',
    hukou_location: '武汉市武昌区',
    current_residence: '武汉市汉口区',
    contact: '13312345678',
    height: 178,
    income: '12k-18k',
    partner_requirement: '有艺术细胞，懂得生活',
    remark: '喜欢创作，追求完美'
  },
  {
    name: '郑十',
    gender: '女',
    age: 33,
    education: '硕士',
    occupation: '律师',
    marital_status: '离异',
    hukou_location: '南京市玄武区',
    current_residence: '南京市秦淮区',
    contact: '13287654321',
    height: 170,
    income: '20k-25k',
    partner_requirement: '有法律意识，尊重女性',
    remark: '工作严谨，生活洒脱'
  },
  {
    name: '王十一',
    gender: '男',
    age: 27,
    education: '大专',
    occupation: '程序员',
    marital_status: '未婚',
    hukou_location: '重庆市渝中区',
    current_residence: '重庆市江北区',
    contact: '13112345678',
    height: 173,
    income: '15k-18k',
    partner_requirement: '活泼开朗，理解技术工作',
    remark: '喜欢编程，偶尔玩游戏'
  },
  {
    name: '李十二',
    gender: '女',
    age: 24,
    education: '本科',
    occupation: '财务',
    marital_status: '未婚',
    hukou_location: '天津市和平区',
    current_residence: '天津市河西区',
    contact: '13087654321',
    height: 160,
    income: '9k-12k',
    partner_requirement: '稳重踏实，有理财观念',
    remark: '做事认真，喜欢烹饪'
  }
];

// 插入数据的函数
async function insertData(data) {
  try {
    const response = await fetch('http://localhost:8000/api/members', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || '提交失败');
    }

    const result = await response.json();
    console.log(`插入成功: ${data.name}`);
    return result;
  } catch (error) {
    console.error(`插入失败 ${data.name}:`, error.message);
    return null;
  }
}

// 批量插入数据
async function batchInsertData() {
  console.log('开始插入模拟数据...');
  const results = [];

  for (const data of mockData) {
    const result = await insertData(data);
    results.push(result);
    // 避免请求过快，添加小延迟
    await new Promise(resolve => setTimeout(resolve, 100));
  }

  const successCount = results.filter(r => r !== null).length;
  console.log(`\n插入完成: 成功 ${successCount} 条，失败 ${mockData.length - successCount} 条`);
}

// 执行批量插入
batchInsertData();
