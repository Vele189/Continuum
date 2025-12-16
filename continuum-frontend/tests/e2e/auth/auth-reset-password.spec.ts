import { test, expect } from "@playwright/test";
import { routes, selectors, validation_messages_for_input} from "./constants";

test.describe('Reset Password Page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(routes.resetPassword);
  });

  //====================================Should render all expected elements========================================================
  test('Should render all expected elements', async ({ page }) => {
    // Check page heading
    await expect(page.locator('h1')).toContainText('Change Password');
    
    // Check logo and platform name
    await expect(page.locator('img[alt="Continuum Logo"]')).toBeVisible();
    await expect(page.locator('span:has-text("Continuum")')).toBeVisible();
    
    // Check description text
    await expect(page.locator('p.text-gray-600')).toContainText('Enter a new password below');
    
    // Check form labels
    await expect(page.locator('label[for="new-password"]')).toContainText('New password*');
    await expect(page.locator('label[for="confirm-password"]')).toContainText('Re-enter new password*');
    
    // Check password input fields
    await expect(page.locator(selectors.new_password_input)).toBeVisible();
    await expect(page.locator('input#confirm-password')).toBeVisible();
    
    // Check password visibility toggles (should have 2, both visible)
    const toggleButtons = page.locator(selectors.show_password_button);
    await expect(toggleButtons).toHaveCount(2);
    await expect(toggleButtons.first()).toBeVisible();
    await expect(toggleButtons.nth(1)).toBeVisible();
    
    // Check submit button
    await expect(page.locator('button:has-text("Change password")')).toBeVisible();
  });

  //====================================Should validate empty fields========================================================
  test('should validate empty new password field', async ({ page }) => {
    const newPasswordInput = page.locator(selectors.new_password_input);
    
    // Fill only confirm password (leave new password empty)
    await page.locator('input#confirm-password').fill('SomePassword123!');
    await page.locator(selectors.submit_button).click();
    
    // Check HTML5 validation
    const validationMessage = await newPasswordInput.evaluate((el: HTMLInputElement) => el.validationMessage);
    expect(validationMessage).toBeTruthy();
    expect(validationMessage.length).toBeGreaterThan(0);
  });

  test('should validate empty confirm password field', async ({ page }) => {
    const confirmPasswordInput = page.locator('input#confirm-password');
    
    // Fill only new password (leave confirm password empty)
    await page.locator(selectors.new_password_input).fill('SomePassword123!');
    await page.locator(selectors.submit_button).click();
    
    // Check HTML5 validation
    const validationMessage = await confirmPasswordInput.evaluate((el: HTMLInputElement) => el.validationMessage);
    expect(validationMessage).toBeTruthy();
    expect(validationMessage.length).toBeGreaterThan(0);
  });

  //====================================Should validate password requirements========================================================
  test('should validate password minimum length (10 characters)', async ({ page }) => {
    const shortPassword = 'Short1!'; // 7 characters
    
    await page.locator(selectors.new_password_input).fill(shortPassword);
    await page.locator('input#confirm-password').fill(shortPassword);
    await page.locator(selectors.submit_button).click();
    
    // Should show error message about length
    await expect(page.locator(selectors.error_message)).toBeVisible();
    await expect(page.locator(selectors.error_message)).toContainText(validation_messages_for_input.password_is_too_short);
  });

  test('should accept password with exactly 10 characters', async ({ page }) => {
    const minPassword = 'Pass123456'; // Exactly 10 characters
    
    await page.locator(selectors.new_password_input).fill(minPassword);
    await page.locator('input#confirm-password').fill(minPassword);
    await page.locator(selectors.submit_button).click();
    
    // Should succeed (show success message after loading)
    await expect(page.locator(selectors.success_message)).toBeVisible({ timeout: 3000 });
  });

  test('should validate password mismatch', async ({ page }) => {
    await page.locator(selectors.new_password_input).fill('ValidPassword123!');
    await page.locator('input#confirm-password').fill('DifferentPassword123!');
    await page.locator(selectors.submit_button).click();
    
    // Should show error message about mismatch
    await expect(page.locator(selectors.error_message)).toBeVisible();
    await expect(page.locator(selectors.error_message)).toContainText(validation_messages_for_input.passwords_mismatch);
  });

  //====================================Should toggle password visibility========================================================
  test('should toggle new password visibility', async ({ page }) => {
    const newPasswordInput = page.locator(selectors.new_password_input);
    const toggleButton = page.locator(selectors.show_password_button).first();
    
    await newPasswordInput.fill('TestPassword123!');
    
    // Initially password should be hidden
    await expect(newPasswordInput).toHaveAttribute('type', 'password');
    
    // Click toggle to show password
    await toggleButton.click();
    await expect(newPasswordInput).toHaveAttribute('type', 'text');
    
    // Click again to hide password
    await toggleButton.click();
    await expect(newPasswordInput).toHaveAttribute('type', 'password');
  });

  test('should toggle confirm password visibility', async ({ page }) => {
    const confirmPasswordInput = page.locator('input#confirm-password');
    const toggleButton = page.locator(selectors.show_password_button).nth(1);
    
    await confirmPasswordInput.fill('TestPassword123!');
    
    // Initially password should be hidden
    await expect(confirmPasswordInput).toHaveAttribute('type', 'password');
    
    // Click toggle to show password
    await toggleButton.click();
    await expect(confirmPasswordInput).toHaveAttribute('type', 'text');
    
    // Click again to hide password
    await toggleButton.click();
    await expect(confirmPasswordInput).toHaveAttribute('type', 'password');
  });

   });
