import { Page } from 'puppeteer';
import { CreateConfig } from '../../config/create-config';
import { LabelsLayer } from './labels.layer';
export declare class StatusLayer extends LabelsLayer {
    page: Page;
    constructor(page: Page, session?: string, options?: CreateConfig);
    /**
     * Send a image message to status stories
     * @category Status
     *
     * @example
     * ```javascript
     * client.sendImageStatus('data:image/jpeg;base64,<a long base64 file...>');
     * ```
     * @param pathOrBase64 Path or base 64 image
     */
    sendImageStatus(pathOrBase64: string): Promise<void>;
    /**
     * Send a video message to status stories
     * @category Status
     *
     * @example
     * ```javascript
     * client.sendVideoStatus('data:video/mp4;base64,<a long base64 file...>');
     * ```
     * @param pathOrBase64 Path or base 64 image
     */
    sendVideoStatus(pathOrBase64: string): Promise<void>;
    /**
     * Send a text to status stories
     * @category Status
     *
     * @example
     * ```javascript
     * client.sendTextStatus(`Bootstrap primary color: #0275d8`, { backgroundColor: '#0275d8', font: 2});
     * ```
     * @param pathOrBase64 Path or base 64 image
     */
    sendTextStatus(text: string, options: string): Promise<void>;
    /**
     * Mark status as read/seen
     * @category Status
     *
     * @example
     * ```javascript
     * client.sendReadStatus('[phone_number]@c.us', 'false_status@broadcast_3A169E0FD4BC6E92212F_[]@c.us');
     * ```
     * @param chatId Chat ID of contact
     * @param statusId ID of status msg
     */
    sendReadStatus(chatId: string, statusId: string): Promise<void>;
}
