import { test, expect } from "@playwright/test";
import { routes, mock_users, selectors, success_messages, api_endpoints, mock_response } from "./constants";

test.describe('Forgot Password Page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(routes.forgotPassword);
  });

  //====================================Should render all expected input fields.========================================================
  test('Should render all expected input fields', async ({ page }) => {
    // here i am checking the page heading
    await expect(page.locator('h1')).toContainText('Forgot password');
    
    // here i am checking the logo and the platform's name
    await expect(page.locator('img[alt="Continuum Logo"]')).toBeVisible();
    await expect(page.locator('span:has-text("Continuum")')).toBeVisible();
    
    // here i am checking the form inputs
    await expect(page.locator(selectors.email_input)).toBeVisible();
    await expect(page.locator(selectors.email_input)).toHaveAttribute('placeholder', 'e.g. LethaboExample@gmail.com');
    
    // here i am checking the submit button
    await expect(page.locator('button:has-text("Send Reset Link")')).toBeVisible();
    
    // here i am checking the links for signing up and forgot password
    await expect(page.locator(selectors.login_link)).toBeVisible();
  });

  //====================================Should validate empty field========================================================
  test('should validate empty email field', async ({ page }) => {
    const emailInput = page.locator(selectors.email_input);
    
    await page.locator(selectors.submit_button).click();
    
    const validationMessage = await emailInput.evaluate((el: HTMLInputElement) => el.validationMessage);
    expect(validationMessage).toBeTruthy();
    expect(validationMessage.length).toBeGreaterThan(0);
  });

  //====================================Should show client-side validation errors========================================================
  test('should validate invalid email format', async ({ page }) => {
    const emailInput = page.locator(selectors.email_input);
    
    await emailInput.fill('invalid-email');
    
    const validationMessage = await emailInput.evaluate((el: HTMLInputElement) => el.validationMessage);
    expect(validationMessage).toBeTruthy();
  });

  //====================================Should allow successful submission with mock data========================================================
  test('should allow successful submission with mock data', async ({ page }) => {
    const emailInput = page.locator(selectors.email_input);
    await emailInput.fill(mock_users.valid_user.email);
    
    const submitButton = page.locator(selectors.submit_button);
    await submitButton.click();
    
    
    await expect(submitButton).toHaveText('Sending...');
    await expect(submitButton).toBeDisabled();
    
    const successMessage = page.locator('div[class*="bg-green-50"]');
    await expect(successMessage).toBeVisible({ timeout: 3000 });
    await expect(successMessage).toContainText(success_messages.reset_link_sent);
  
    await expect(emailInput).not.toBeVisible();
  });

}); 