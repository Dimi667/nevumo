#!/usr/bin/env node

/**
 * Test script to validate photo upload functionality
 * Run with: node test_photo_upload.js
 */

const fs = require('fs');
const path = require('path');

// Test configuration
const API_BASE = 'http://localhost:8000';
const WEB_BASE = 'http://localhost:3000';

async function testPhotoUpload() {
  console.log('🧪 Testing Photo Upload Functionality\n');
  
  // Test 1: Check API server is running
  console.log('1. Testing API server...');
  try {
    const response = await fetch(`${API_BASE}/docs`);
    if (response.ok) {
      console.log('✅ API server is running');
    } else {
      throw new Error('API server not responding');
    }
  } catch (error) {
    console.log('❌ API server test failed:', error.message);
    return;
  }

  // Test 2: Check static file serving
  console.log('\n2. Testing static file serving...');
  try {
    const staticResponse = await fetch(`${API_BASE}/static/provider_images/6200e333-0a45-4531-9a65-90ac6a46f38a.png`);
    if (staticResponse.ok) {
      console.log('✅ Static file serving works');
      console.log(`   Content-Type: ${staticResponse.headers.get('content-type')}`);
      console.log(`   Content-Length: ${staticResponse.headers.get('content-length')} bytes`);
    } else {
      throw new Error(`Static file serving failed: ${staticResponse.status}`);
    }
  } catch (error) {
    console.log('❌ Static file serving test failed:', error.message);
  }

  // Test 3: Check web server
  console.log('\n3. Testing web server...');
  try {
    const webResponse = await fetch(`${WEB_BASE}`);
    if (webResponse.ok) {
      console.log('✅ Web server is running');
    } else {
      throw new Error('Web server not responding');
    }
  } catch (error) {
    console.log('❌ Web server test failed:', error.message);
  }

  // Test 4: Test CORS (simple check)
  console.log('\n4. Testing CORS configuration...');
  try {
    const corsResponse = await fetch(`${API_BASE}/api/v1/categories`, {
      method: 'OPTIONS',
      headers: {
        'Origin': WEB_BASE,
        'Access-Control-Request-Method': 'GET',
        'Access-Control-Request-Headers': 'Content-Type'
      }
    });
    
    const corsHeaders = corsResponse.headers.get('access-control-allow-origin');
    if (corsHeaders && corsHeaders.includes('localhost:3000')) {
      console.log('✅ CORS is configured correctly');
    } else {
      console.log('⚠️  CORS might need configuration');
    }
  } catch (error) {
    console.log('❌ CORS test failed:', error.message);
  }

  console.log('\n🎯 Manual Testing Instructions:');
  console.log('1. Open http://localhost:3000/en/provider/dashboard/profile');
  console.log('2. Try uploading a new profile picture');
  console.log('3. Check browser console for detailed logging');
  console.log('4. Verify image loads correctly after upload');
  console.log('5. Test error scenarios (large file, wrong format)');
  
  console.log('\n📊 Expected Behavior:');
  console.log('- Upload should work with JPG/PNG/WebP files under 5MB');
  console.log('- Image should load immediately after upload');
  console.log('- Console should show detailed logging');
  console.log('- Errors should have user-friendly messages');
  console.log('- Failed loads should retry automatically');
}

// Run the test
testPhotoUpload().catch(console.error);
