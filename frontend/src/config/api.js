// API配置文件
// 动态获取API地址（同源访问）
export const API_BASE_URL = `${window.location.protocol}//${window.location.hostname}:8000/api`

// 请求封装
const request = {
  get: async (url) => {
    const response = await fetch(`${API_BASE_URL}${url}`)
    if (!response.ok) throw new Error('请求失败')
    return response.json()
  },
  post: async (url, data) => {
    const response = await fetch(`${API_BASE_URL}${url}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    if (!response.ok) throw new Error('请求失败')
    return response.json()
  },
  put: async (url, data) => {
    const response = await fetch(`${API_BASE_URL}${url}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    if (!response.ok) throw new Error('请求失败')
    return response.json()
  },
  delete: async (url) => {
    const response = await fetch(`${API_BASE_URL}${url}`, {
      method: 'DELETE'
    })
    if (!response.ok) throw new Error('请求失败')
    return response.json()
  }
}

// 用户管理
export const getUsers = () => request.get('/users')
export const createUser = (data) => request.post('/users', data)
export const updateUser = (id, data) => request.put(`/users/${id}`, data)
export const deleteUser = (id) => request.delete(`/users/${id}`)

// 会员管理
export const getMembers = () => request.get('/members')
export const createMember = (data) => request.post('/members', data)
export const updateMember = (id, data) => request.put(`/members/${id}`, data)
export const deleteMember = (id) => request.delete(`/members/${id}`)

// 菜单管理
export const getMenus = () => request.get('/menus')
export const createMenu = (data) => request.post('/menus', data)
export const updateMenu = (id, data) => request.put(`/menus/${id}`, data)
export const deleteMenu = (id) => request.delete(`/menus/${id}`)

// 角色管理
export const getRoles = () => request.get('/roles')
export const createRole = (data) => request.post('/roles', data)
export const updateRole = (id, data) => request.put(`/roles/${id}`, data)
export const deleteRole = (id) => request.delete(`/roles/${id}`)
export const getRoleMenus = (roleId) => request.get(`/roles/${roleId}/menus`)
export const assignRoleMenus = (roleId, menuIds) => request.put(`/roles/${roleId}/menus`, { menu_ids: menuIds })