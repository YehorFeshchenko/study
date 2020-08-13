import CreateContactDto from "../../dto/create-contact.dto";
import Contact from './contact.entity';
import { ContactsService } from './contacts.service';
export declare class ContactsController {
    private readonly contactsService;
    constructor(contactsService: ContactsService);
    create(createContactDto: CreateContactDto): Promise<Contact>;
    findAll(): Promise<Contact[]>;
    findOne(id: string): Promise<Contact>;
    remove(id: string): Promise<void>;
}
