import { test } from '@playwright/test';

test('provider lead status full diagnostic', async ({ request }) => {
  // Login
  const loginRes = await request.post('http://192.168.0.15:8000/api/v1/auth/login', {
    data: { email: 'lili@test.bg', password: '123456789' }
  });
  const loginData = await loginRes.json();
  if (!loginData?.data?.token) { console.log('LOGIN FAILED'); return; }
  const token = loginData.data.token;
  console.log('=== LOGIN OK, role:', loginData.data.user.role);

  const headers = { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' };

  // Get leads
  const leadsRes = await request.get('http://192.168.0.15:8000/api/v1/provider/leads?limit=100', { headers });
  const leadsData = await leadsRes.json();
  const items = leadsData?.data?.leads ?? leadsData?.data?.items ?? [];
  console.log('=== TOTAL LEADS:', items.length);

  // Count by status
  const byStatus: Record<string, number> = {};
  for (const l of items) {
    byStatus[l.status] = (byStatus[l.status] ?? 0) + 1;
  }
  console.log('=== STATUS COUNTS:', JSON.stringify(byStatus));

  // Try each valid transition
  const transitions: Array<{ fromStatus: string; toStatus: string }> = [
    { fromStatus: 'created', toStatus: 'contacted' },
    { fromStatus: 'pending_match', toStatus: 'contacted' },
    { fromStatus: 'matched', toStatus: 'contacted' },
    { fromStatus: 'contacted', toStatus: 'cancelled' },
    { fromStatus: 'created', toStatus: 'cancelled' },
  ];

  for (const { fromStatus, toStatus } of transitions) {
    const lead = items.find((l: { status: string }) => l.status === fromStatus);
    if (!lead) {
      console.log(`=== SKIP: no lead with status '${fromStatus}'`);
      continue;
    }

    const res = await request.patch(
      `http://192.168.0.15:8000/api/v1/provider/leads/${lead.id}`,
      { headers, data: { status: toStatus } }
    );
    const body = await res.json();
    console.log(`=== PATCH ${fromStatus} → ${toStatus} | HTTP ${res.status()} | ${JSON.stringify(body)}`);

    // Reset lead back for next test
    if (res.status() === 200) {
      await request.patch(
        `http://192.168.0.15:8000/api/v1/provider/leads/${lead.id}`,
        { headers, data: { status: fromStatus === 'contacted' ? 'contacted' : fromStatus } }
      );
    }
  }
});
