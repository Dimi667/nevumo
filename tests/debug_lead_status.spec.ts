import { test } from '@playwright/test';

test('debug lead status update', async ({ page, request }) => {
  // Step 1: Login via API to get token
  const loginRes = await request.post('http://192.168.0.15:8000/api/v1/auth/login', {
    data: { email: 'lili@test.bg', password: '123456789' }
  });
  const loginData = await loginRes.json();
  console.log('LOGIN STATUS:', loginRes.status());
  console.log('LOGIN BODY:', JSON.stringify(loginData));

  if (!loginData?.data?.token) {
    console.log('LOGIN FAILED — check credentials');
    return;
  }

  const token = loginData.data.token;
  console.log('TOKEN OK');

  // Step 2: Get leads
  const leadsRes = await request.get('http://192.168.0.15:8000/api/v1/client/leads', {
    headers: { Authorization: `Bearer ${token}` }
  });
  const leadsData = await leadsRes.json();
  console.log('LEADS STATUS:', leadsRes.status());

  if (!leadsData?.data?.items?.length) {
    console.log('NO LEADS FOUND');
    return;
  }

  const lead = leadsData.data.items[0];
  console.log('LEAD:', JSON.stringify({ id: lead.id, status: lead.status, cancelled_by: lead.cancelled_by }));

  // Step 3: PATCH status → contacted
  const patchRes = await request.patch(`http://192.168.0.15:8000/api/v1/client/leads/${lead.id}/status`, {
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    data: { status: 'contacted' }
  });
  const patchData = await patchRes.json();
  console.log('PATCH STATUS:', patchRes.status());
  console.log('PATCH BODY:', JSON.stringify(patchData));

  // Step 4: Get leads again
  const afterRes = await request.get('http://192.168.0.15:8000/api/v1/client/leads', {
    headers: { Authorization: `Bearer ${token}` }
  });
  const afterData = await afterRes.json();
  const afterLead = afterData.data.items[0];
  console.log('STATUS AFTER:', afterLead?.status);
});
