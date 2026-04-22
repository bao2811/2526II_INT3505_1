import http from 'k6/http';
import { check, sleep } from 'k6';

const baseUrl = __ENV.BASE_URL || 'https://jsonplaceholder.typicode.com';

export const options = {
  scenarios: {
    users_api_load: {
      executor: 'constant-vus',
      vus: 50,
      duration: '30s',
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['avg<1000', 'p(95)<1500'],
    checks: ['rate>0.99'],
  },
};

export default function () {
  const response = http.get(`${baseUrl}/users`, {
    tags: {
      endpoint: 'GET /users',
      suite: 'week8-performance',
    },
  });

  check(response, {
    'status is 200': (r) => r.status === 200,
    'response has body': (r) => !!r.body,
  });

  sleep(1);
}
