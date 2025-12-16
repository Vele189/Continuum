import { test, expect } from "@playwright/test";
import { routes, mock_users, selectors, mock_response } from "./constants";


test.describe('Register Page', () => {
    test.beforeEach(async ({ page }) => {
        await page.goto(routes.register);
    });


    test('Should render all required input fields', async ({ page }) => {
            // here i am checking the page heading
    await expect(page.locator('h1')).toContainText('Create your account');
    
    // here i am checking the logo and the platform's name
    await expect(page.locator('img[alt="Continuum Logo"]')).toBeVisible();
    await expect(page.locator('span:has-text("Continuum")')).toBeVisible();


    // here i am checking the form inputs
    await expect(page.locator(selectors.firstname_input)).toBeVisible();
    await expect(page.locator(selectors.firstname_input)).toHaveAttribute('placeholder', 'e.g. Lethabo Edmond');
    await expect(page.locator(selectors.lastname_input)).toBeVisible();
    await expect(page.locator(selectors.lastname_input)).toHaveAttribute('placeholder', 'e.g. Sehlapelo');
    await expect(page.locator(selectors.email_input)).toBeVisible();
    await expect(page.locator(selectors.email_input)).toHaveAttribute('placeholder', 'e.g. LethaboExample@gmail.com');
     await expect(page.locator('input#password')).toBeVisible();
    await expect(page.locator('input#password')).toHaveAttribute('placeholder', '••••••••');
    
    await expect(page.locator('input#confirm-password')).toBeVisible();
    await expect(page.locator('input#confirm-password')).toHaveAttribute('placeholder', '••••••••');
    
    // Check password visibility toggles (should have 2, both visible)
    const toggleButtons = page.locator(selectors.show_password_button);
    await expect(toggleButtons).toHaveCount(2);
    await expect(toggleButtons.first()).toBeVisible();
    await expect(toggleButtons.nth(1)).toBeVisible();

    // here i am checking the submit button
    await expect(page.locator('button:has-text("Sign Up")')).toBeVisible();
       // here i am checking the links for signing up and forgot password
    await expect(page.locator(selectors.login_link)).toBeVisible();
    
    // here i am checking the terms and policy links
    await expect(page.locator('a:has-text("Terms of Service")')).toBeVisible();
    await expect(page.locator('a:has-text("Privacy Policy")')).toBeVisible();
  });


//====================================Should validate empty field========================================================
    test('should validate empty firstname field', async ({ page }) => {
    const firstnameInput = page.locator(selectors.firstname_input);
    

    await page.locator(selectors.lastname_input).fill(mock_users.valid_user.lastname);
    await page.locator(selectors.email_input).fill(mock_users.valid_user.email);
    await page.locator('input#password').fill(mock_users.valid_user.password);
    await page.locator('input#confirm-password').fill(mock_users.valid_user.password);
    await page.locator(selectors.submit_button).click();
    
    const validationMessage = await firstnameInput.evaluate((el: HTMLInputElement) => el.validationMessage);
    expect(validationMessage).toBeTruthy();
    expect(validationMessage.length).toBeGreaterThan(0);
  });

    test('should validate empty lastname field', async ({ page }) => {
    const lastnameInput = page.locator(selectors.lastname_input);
    
    await page.locator(selectors.firstname_input).fill(mock_users.valid_user.firstname);
    await page.locator(selectors.email_input).fill(mock_users.valid_user.email);
    await page.locator('input#password').fill(mock_users.valid_user.password);
    await page.locator('input#confirm-password').fill(mock_users.valid_user.password);
    await page.locator(selectors.submit_button).click();
    
    const validationMessage = await lastnameInput.evaluate((el: HTMLInputElement) => el.validationMessage);
    expect(validationMessage).toBeTruthy();
    expect(validationMessage.length).toBeGreaterThan(0);
  });

test('should validate empty email field', async ({ page }) => {
    const emailInput = page.locator(selectors.email_input);
    
    await page.locator(selectors.firstname_input).fill(mock_users.valid_user.firstname);
    await page.locator(selectors.lastname_input).fill(mock_users.valid_user.lastname);
    await page.locator('input#password').fill(mock_users.valid_user.password);
    await page.locator('input#confirm-password').fill(mock_users.valid_user.password);
    await page.locator(selectors.submit_button).click();
    
    const validationMessage = await emailInput.evaluate((el: HTMLInputElement) => el.validationMessage);
    expect(validationMessage).toBeTruthy();
    expect(validationMessage.length).toBeGreaterThan(0);
  });

  test('should validate empty password field', async ({ page }) => {
    const passwordInput = page.locator('input#password');
    
   await page.locator(selectors.firstname_input).fill(mock_users.valid_user.firstname);
    await page.locator(selectors.lastname_input).fill(mock_users.valid_user.lastname);
    await page.locator(selectors.email_input).fill(mock_users.valid_user.email);
    await page.locator('input#confirm-password').fill(mock_users.valid_user.password);
    await page.locator(selectors.submit_button).click();
    
    const validationMessage = await passwordInput.evaluate((el: HTMLInputElement) => el.validationMessage);
    expect(validationMessage).toBeTruthy();
    expect(validationMessage.length).toBeGreaterThan(0);
  });

    test('should validate empty confirm password field', async ({ page }) => {
    const passwordInput = page.locator('input#confirm-password');
    
   await page.locator(selectors.firstname_input).fill(mock_users.valid_user.firstname);
    await page.locator(selectors.lastname_input).fill(mock_users.valid_user.lastname);
    await page.locator(selectors.email_input).fill(mock_users.valid_user.email);
    await page.locator('input#password').fill(mock_users.valid_user.password);
    await page.locator(selectors.submit_button).click();
    
    const validationMessage = await passwordInput.evaluate((el: HTMLInputElement) => el.validationMessage);
    expect(validationMessage).toBeTruthy();
    expect(validationMessage.length).toBeGreaterThan(0);
  });


  //====================================Should show client-side validation errors========================================================
test('should validate Password mismatch', async ({ page }) => {
    const passwordInput = page.locator('input#password');
    const confirmPasswordInput = page.locator('input#confirm-password');
    
    await passwordInput.fill(mock_users.valid_user.password);
    await confirmPasswordInput.fill(mock_users.invalid_user.password);
    await page.locator(selectors.firstname_input).fill(mock_users.valid_user.firstname);
    await page.locator(selectors.lastname_input).fill(mock_users.valid_user.lastname);
    await page.locator(selectors.email_input).fill(mock_users.valid_user.email);
    
    await page.locator(selectors.submit_button).click();
    
expect(page.url()).toContain(routes.register);

  });

  test('should validate invalid email format', async ({ page }) => {
    const emailInput = page.locator(selectors.email_input);
    
    await emailInput.fill('invalid-email');
    await page.locator(selectors.firstname_input).fill(mock_users.valid_user.firstname);
    await page.locator(selectors.lastname_input).fill(mock_users.valid_user.lastname);
    await page.locator('input#password').fill(mock_users.valid_user.password);
    await page.locator('input#confirm-password').fill(mock_users.valid_user.password);
    await page.locator(selectors.submit_button).click();
    
  
    const validationMessage = await emailInput.evaluate((el: HTMLInputElement) => el.validationMessage);
    expect(validationMessage).toBeTruthy();
  });

 

  test('should toggle password visibility', async ({ page }) => {
    const passwordInput = page.locator('input#password');
    const toggleButton = page.locator(selectors.show_password_button).first();
    
    await passwordInput.fill(mock_users.valid_user.password);
    
    // Initial state should be 'password' type (hidden)
    await expect(passwordInput).toHaveAttribute('type', 'password');
    
    // First click should show the password (change to 'text')
    await toggleButton.click();
    await expect(passwordInput).toHaveAttribute('type', 'text');

    
    await toggleButton.click();
    await expect(passwordInput).toHaveAttribute('type', 'password');
  });

    test('should toggle confirm password visibility', async ({ page }) => {
    const passwordInput = page.locator('input#confirm-password');
    const toggleButton = page.locator(selectors.show_password_button).last();
    
    await passwordInput.fill(mock_users.valid_user.password);
    
    // Initial state should be 'password' type (hidden)
    await expect(passwordInput).toHaveAttribute('type', 'password');
    
    // First click should show the password (change to 'text')
    await toggleButton.click();
    await expect(passwordInput).toHaveAttribute('type', 'text');

    
    await toggleButton.click();
    await expect(passwordInput).toHaveAttribute('type', 'password');
  });


    test('Should allow successful submission with mock data.', async ({ page }) => {
        await page.route('**/**/api/auth/register', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(mock_response.register.success.body),
      });
    });

    await page.goto(routes.register);

    // Fill all fields with valid data
    await page.locator(selectors.firstname_input).fill(mock_users.valid_user.firstname);
    await page.locator(selectors.lastname_input).fill(mock_users.valid_user.lastname);
    await page.locator(selectors.email_input).fill(mock_users.valid_user.email);
    await page.locator('input#password').fill(mock_users.valid_user.password);
    await page.locator('input#confirm-password').fill(mock_users.valid_user.password);
    
    await page.locator(selectors.submit_button).click();
    
    // Verify navigation to dashboard
    await page.waitForURL(routes.dashboard, { timeout: 10000 });
    expect(page.url()).toContain(routes.dashboard);
  });

  test('Should show error on registration failure', async ({ page }) => {
    // Mock failed registration API
    await page.route('**/**/api/auth/register', async (route) => {
      await route.fulfill({
        status: 400,
        contentType: 'application/json',
        body: JSON.stringify(mock_response.register.failure.body),
      });
    });

    await page.goto(routes.register);

    // Fill all fields
    await page.locator(selectors.firstname_input).fill(mock_users.valid_user.firstname);
    await page.locator(selectors.lastname_input).fill(mock_users.valid_user.lastname);
    await page.locator(selectors.email_input).fill(mock_users.valid_user.email);
    await page.locator('input#password').fill(mock_users.valid_user.password);
    await page.locator('input#confirm-password').fill(mock_users.valid_user.password);
    
    await page.locator(selectors.submit_button).click();
    
    // Wait for the request to complete
    await page.waitForSelector('button:has-text("Sign Up")', { timeout: 5000 });
    
    // Should still be on register page
    expect(page.url()).toContain(routes.register);
  });

  test('should navigate to login page', async ({ page }) => {
    await page.locator(selectors.login_link).click();
    await page.waitForURL(routes.login);
    expect(page.url()).toContain(routes.login);
  });
});
    
