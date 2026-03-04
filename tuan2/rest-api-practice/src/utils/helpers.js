// src/utils/helpers.js
// Cac ham tien ich dung chung

/**
 * Phan trang mang
 * @param {Array} array - Mang day du
 * @param {number} page - So trang (bat dau tu 1)
 * @param {number} limit - So phan tu moi trang
 * @returns {{ data, pagination }}
 */
const paginate = (array, page = 1, limit = 10) => {
  page = Math.max(1, parseInt(page) || 1);
  limit = Math.max(1, Math.min(100, parseInt(limit) || 10));

  const total = array.length;
  const totalPages = Math.ceil(total / limit);
  const offset = (page - 1) * limit;
  const data = array.slice(offset, offset + limit);

  return {
    data,
    pagination: {
      page,
      limit,
      total,
      totalPages,
      hasNext: page < totalPages,
      hasPrev: page > 1,
    },
  };
};

/**
 * Tao ETag don gian tu noi dung
 * @param {any} data
 * @returns {string}
 */
const generateETag = (data) => {
  const str = JSON.stringify(data);
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = (hash << 5) - hash + str.charCodeAt(i);
    hash |= 0;
  }
  return `"${Math.abs(hash).toString(16)}"`;
};

/**
 * Validate email don gian
 */
const isValidEmail = (email) => {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
};

/**
 * Loc bo truong deletedAt khoi object tra ve cho client
 */
const sanitize = (obj) => {
  if (!obj) return obj;
  const { deletedAt, ...rest } = obj;
  return rest;
};

module.exports = { paginate, generateETag, isValidEmail, sanitize };
